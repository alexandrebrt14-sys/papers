# -*- coding: utf-8 -*-
import sqlite3, json, math
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf

DB = r'C:/Users/alexa/AppData/Local/Temp/planb/data/papers.db'
con = sqlite3.connect(DB)

# Core sample = no probes, no calibration
df = pd.read_sql_query("""
SELECT id, llm, vertical, query_category, query_lang, query_type,
       cited_v2, cited_count_v2, cited_entities_v2_json,
       response_length_chars_v2, source_count, token_count, latency_ms,
       is_probe, is_calibration, timestamp
FROM citations
WHERE COALESCE(is_probe,0)=0 AND COALESCE(is_calibration,0)=0
""", con)
con.close()

print("CORE n=", len(df), "cited_v2=", int(df.cited_v2.sum()),
      "rate=%.4f" % df.cited_v2.mean())

def wilson(k, n, z=1.96):
    if n == 0: return (float('nan'),)*3
    p = k/n
    denom = 1 + z*z/n
    center = (p + z*z/(2*n))/denom
    half = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/denom
    return p, center-half, center+half

# ---------- (A) Leave-one-out Nubank ----------
# For each fintech response that is cited, parse entities. If the ONLY cited
# entity is Nubank (canonical forms), recount as not-cited under LOO.
def parse_entities(j):
    if not j: return []
    try:
        data = json.loads(j)
    except Exception:
        return []
    out = []
    if isinstance(data, dict):
        # could be {entity: count} or {"entities":[...]}
        if 'entities' in data and isinstance(data['entities'], list):
            for e in data['entities']:
                if isinstance(e, str): out.append(e)
                elif isinstance(e, dict):
                    out.append(e.get('name') or e.get('entity') or e.get('canonical') or '')
        else:
            out = list(data.keys())
    elif isinstance(data, list):
        for e in data:
            if isinstance(e, str): out.append(e)
            elif isinstance(e, dict):
                out.append(e.get('name') or e.get('entity') or e.get('canonical') or '')
    return [str(x).strip() for x in out if str(x).strip()]

fin = df[df.vertical == 'fintech'].copy()
# inspect a few entity json samples
samples = fin[fin.cited_v2==1]['cited_entities_v2_json'].dropna().head(5).tolist()
print("SAMPLE entity json:")
for s in samples:
    print("  ", s[:200])

NUBANK = {'nubank','nu bank','nu','nu pagamentos','nu holdings','roxinho'}
def is_nubank(name):
    return name.lower().strip() in NUBANK

fin['ents'] = fin['cited_entities_v2_json'].apply(parse_entities)
fin['n_ents'] = fin['ents'].apply(len)
def only_nubank(row):
    if row['cited_v2'] != 1: return False
    ents = row['ents']
    if not ents:
        return False
    return all(is_nubank(e) for e in ents)
fin['only_nubank'] = fin.apply(only_nubank, axis=1)

# LOO: a response counts as cited under LOO if cited_v2==1 AND not only-nubank
fin['cited_loo'] = fin['cited_v2'] & (~fin['only_nubank'])
n_fin = len(fin)
k_orig = int(fin.cited_v2.sum())
k_loo = int(fin.cited_loo.sum())
n_only_nu = int(fin.only_nubank.sum())
# Also: strip Nubank from any entity counting -> "fintech minus Nubank presence"
def cited_no_nu(row):
    if row['cited_v2'] != 1: return 0
    rest = [e for e in row['ents'] if not is_nubank(e)]
    return 1 if len(rest) > 0 else 0
fin['cited_dropnu'] = fin.apply(cited_no_nu, axis=1)
k_dropnu = int(fin.cited_dropnu.sum())

print("\n=== LOO NUBANK (fintech) ===")
p,lo,hi = wilson(k_orig, n_fin)
print("Original fintech: %d/%d = %.4f (IC95 %.4f-%.4f)" % (k_orig,n_fin,p,lo,hi))
print("Only-Nubank responses (cited, sole entity Nubank): %d (%.2f%% of all fintech, %.2f%% of cited)"
      % (n_only_nu, 100*n_only_nu/n_fin, 100*n_only_nu/k_orig))
p,lo,hi = wilson(k_loo, n_fin)
print("LOO (drop sole-Nubank responses): %d/%d = %.4f (IC95 %.4f-%.4f)" % (k_loo,n_fin,p,lo,hi))
p,lo,hi = wilson(k_dropnu, n_fin)
print("Drop-Nubank-presence (cited iff >=1 non-Nubank entity): %d/%d = %.4f (IC95 %.4f-%.4f)" % (k_dropnu,n_fin,p,lo,hi))

# Compare LOO fintech vs varejo (the closest competitor)
var = df[df.vertical=='varejo']
k_var = int(var.cited_v2.sum()); n_var = len(var)
p,lo,hi = wilson(k_var, n_var)
print("Varejo (orig): %d/%d = %.4f (IC95 %.4f-%.4f)" % (k_var,n_var,p,lo,hi))

# chi2 fintech-LOO vs varejo
tbl = np.array([[k_loo, n_fin-k_loo],[k_var, n_var-k_var]])
chi2,pval,_,_ = stats.chi2_contingency(tbl, correction=False)
print("LOO-fintech vs varejo: chi2=%.2f p=%.3g" % (chi2,pval))
tbl2 = np.array([[k_dropnu, n_fin-k_dropnu],[k_var, n_var-k_var]])
chi2b,pvalb,_,_ = stats.chi2_contingency(tbl2, correction=False)
print("DropNu-fintech vs varejo: chi2=%.2f p=%.3g" % (chi2b,pvalb))

# ---------- (B) Per-entity-query normalization ----------
# rate normalized by roster size: cited responses / roster entities
roster = {'fintech':19,'varejo':15,'tecnologia':15,'saude':15}
print("\n=== PER-ENTITY-QUERY NORMALIZATION ===")
for v in ['fintech','varejo','tecnologia','saude']:
    sub = df[df.vertical==v]
    k = int(sub.cited_v2.sum()); n=len(sub)
    # total entity mentions
    ents_total = sub['cited_entities_v2_json'].apply(lambda j: len(parse_entities(j))).sum()
    mean_ents = ents_total/n
    rate = k/n
    norm_rate = rate / roster[v]
    print("%s: rate=%.4f, roster=%d, rate/roster=%.5f, mean_entities/resp=%.4f, mentions/entity=%.1f"
          % (v, rate, roster[v], norm_rate, mean_ents, k/roster[v]))

# ---------- (C) Logistic regression cited_v2 ~ vertical + llm + category ----------
print("\n=== LOGISTIC REGRESSION (cited_v2 ~ C(vertical)+C(llm)+C(query_category)) ===")
mdf = df.dropna(subset=['vertical','llm','query_category']).copy()
mdf['cited_v2'] = mdf['cited_v2'].astype(int)
# reference: vertical=saude (lowest), llm=Gemini (lowest), category set alphabetical
mdf['vertical'] = pd.Categorical(mdf['vertical'], categories=['saude','tecnologia','varejo','fintech'])
mdf['llm'] = pd.Categorical(mdf['llm'])
mdf['query_category'] = pd.Categorical(mdf['query_category'])
m1 = smf.logit("cited_v2 ~ C(vertical) + C(llm) + C(query_category)", data=mdf).fit(disp=0)
print(m1.summary2().tables[1].to_string())
# Odds ratios with CI
params = m1.params; conf = m1.conf_int()
ors = pd.DataFrame({'OR':np.exp(params),'OR_lo':np.exp(conf[0]),'OR_hi':np.exp(conf[1])})
print("\nOdds ratios (IC95):")
print(ors.to_string())
print("\nPseudo R2 (McFadden):", m1.prsquared, " N=", int(m1.nobs))

# Model with language + query_type added (robustness)
print("\n=== ROBUSTNESS MODEL (+lang +query_type) ===")
mdf2 = mdf.dropna(subset=['query_lang','query_type']).copy()
m2 = smf.logit("cited_v2 ~ C(vertical) + C(llm) + C(query_category) + C(query_lang) + C(query_type)", data=mdf2).fit(disp=0)
ors2 = pd.DataFrame({'OR':np.exp(m2.params),'OR_lo':np.exp(m2.conf_int()[0]),'OR_hi':np.exp(m2.conf_int()[1])})
print(ors2.loc[[i for i in ors2.index if 'vertical' in i or 'lang' in i or 'query_type' in i]].to_string())
print("Pseudo R2:", m2.prsquared)

# ---------- (D) Mantel-Haenszel: fintech vs varejo stratified by query_category ----------
print("\n=== MANTEL-HAENSZEL (fintech vs varejo, strata=query_category) ===")
pair = df[df.vertical.isin(['fintech','varejo'])].copy()
pair['exposed'] = (pair.vertical=='fintech').astype(int)
num=0.0; den=0.0
mh_rows=[]
for cat, g in pair.groupby('query_category'):
    a = int(((g.exposed==1)&(g.cited_v2==1)).sum())  # fintech cited
    b = int(((g.exposed==1)&(g.cited_v2==0)).sum())
    c = int(((g.exposed==0)&(g.cited_v2==1)).sum())  # varejo cited
    d = int(((g.exposed==0)&(g.cited_v2==0)).sum())
    n = a+b+c+d
    if n==0: continue
    num += a*d/n
    den += b*c/n
    or_strat = (a*d)/(b*c) if b*c>0 else float('nan')
    mh_rows.append((cat,a,b,c,d,or_strat))
or_mh = num/den
print("MH common OR (fintech vs varejo) =", round(or_mh,4))
for r in mh_rows:
    print("  cat=%-12s a=%4d b=%4d c=%4d d=%4d  OR_strata=%.3f" % r)

# ---------- (E) Effect sizes: risk difference & risk ratio fintech vs each ----------
print("\n=== EFFECT SIZES (fintech vs each vertical) ===")
def two_prop(k1,n1,k2,n2):
    p1=k1/n1; p2=k2/n2
    rd=p1-p2
    se=math.sqrt(p1*(1-p1)/n1 + p2*(1-p2)/n2)
    rr=p1/p2
    # OR
    a,b,c,d = k1,n1-k1,k2,n2-k2
    orr=(a*d)/(b*c)
    se_lor=math.sqrt(1/a+1/b+1/c+1/d)
    return rd, rd-1.96*se, rd+1.96*se, rr, orr, math.exp(math.log(orr)-1.96*se_lor), math.exp(math.log(orr)+1.96*se_lor)
kf=int(fin.cited_v2.sum()); nf=len(fin)
for v in ['varejo','tecnologia','saude']:
    sub=df[df.vertical==v]; kv=int(sub.cited_v2.sum()); nv=len(sub)
    rd,rdl,rdh,rr,orr,orl,orh = two_prop(kf,nf,kv,nv)
    print("fintech vs %-11s RD=%+.4f (IC95 %+.4f..%+.4f) RR=%.3f OR=%.3f (IC95 %.3f..%.3f)"
          % (v,rd,rdl,rdh,rr,orr,orl,orh))

# LOO fintech vs each
print("\n--- with LOO fintech rate ---")
for v in ['varejo','tecnologia','saude']:
    sub=df[df.vertical==v]; kv=int(sub.cited_v2.sum()); nv=len(sub)
    rd,rdl,rdh,rr,orr,orl,orh = two_prop(k_loo,nf,kv,nv)
    print("fintech(LOO) vs %-11s RD=%+.4f (IC95 %+.4f..%+.4f) RR=%.3f OR=%.3f"
          % (v,rd,rdl,rdh,rr,orr))

print("\nDONE")
