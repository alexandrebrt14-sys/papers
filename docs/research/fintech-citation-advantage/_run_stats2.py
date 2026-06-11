# -*- coding: utf-8 -*-
import sqlite3, json, math
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf

DB = r'C:/Users/alexa/AppData/Local/Temp/planb/data/papers.db'
con = sqlite3.connect(DB)
df = pd.read_sql_query("""
SELECT id, llm, vertical, query_category, query_lang, query_type,
       cited_v2, cited_entities_v2_json
FROM citations
WHERE COALESCE(is_probe,0)=0 AND COALESCE(is_calibration,0)=0
""", con)
con.close()

def parse_entities(j):
    if not j: return []
    try: data=json.loads(j)
    except: return []
    if isinstance(data,list): return [str(x).strip() for x in data if str(x).strip()]
    if isinstance(data,dict): return [str(x).strip() for x in data.keys()]
    return []

NUBANK={'nubank','nu bank','nu','nu pagamentos','nu holdings','roxinho'}
df['ents']=df['cited_entities_v2_json'].apply(parse_entities)
def only_nu(row):
    if row['cited_v2']!=1: return False
    e=row['ents']
    return bool(e) and all(x.lower() in NUBANK for x in e)
df['only_nubank']=df.apply(only_nu,axis=1)
# LOO outcome: cited_v2 but recode sole-Nubank fintech responses to 0
df['cited_loo']=df['cited_v2'].astype(int)
df.loc[df['only_nubank'],'cited_loo']=0

# ---------- Regression with LOO outcome ----------
print("=== LOGISTIC WITH LOO OUTCOME (cited_loo ~ vertical+llm+category) ===")
mdf=df.dropna(subset=['vertical','llm','query_category']).copy()
mdf['vertical']=pd.Categorical(mdf['vertical'],categories=['saude','tecnologia','varejo','fintech'])
m=smf.logit("cited_loo ~ C(vertical)+C(llm)+C(query_category)",data=mdf).fit(disp=0)
ors=pd.DataFrame({'OR':np.exp(m.params),'lo':np.exp(m.conf_int()[0]),'hi':np.exp(m.conf_int()[1])})
print(ors.loc[[i for i in ors.index if 'vertical' in i]].to_string())
print("Pseudo R2:",round(m.prsquared,4),"N=",int(m.nobs))

# ---------- Breslow-Day homogeneity for MH (fintech vs varejo by category) ----------
print("\n=== BRESLOW-DAY (homogeneidade dos OR por categoria) ===")
pair=df[df.vertical.isin(['fintech','varejo'])].copy()
pair['exp']=(pair.vertical=='fintech').astype(int)
# common MH OR
num=den=0.0
strata=[]
for cat,g in pair.groupby('query_category'):
    a=int(((g.exp==1)&(g.cited_v2==1)).sum());b=int(((g.exp==1)&(g.cited_v2==0)).sum())
    c=int(((g.exp==0)&(g.cited_v2==1)).sum());d=int(((g.exp==0)&(g.cited_v2==0)).sum())
    n=a+b+c+d
    num+=a*d/n; den+=b*c/n
    strata.append((cat,a,b,c,d))
or_mh=num/den
# Breslow-Day statistic
bd=0.0
for cat,a,b,c,d in strata:
    n1=a+b; n0=c+d; m1=a+c; m0=b+d; N=n1+n0
    # expected a under common OR (solve quadratic)
    # A*x^2 + B*x + C = 0 for E[a]
    A=or_mh-1
    B=-(or_mh*(n1+m1)+(n0-m1))
    Cc=or_mh*n1*m1
    if abs(A)<1e-9:
        Ea=n1*m1/N
    else:
        disc=B*B-4*A*Cc
        Ea=(-B-math.sqrt(disc))/(2*A)
    Va=1/(1/Ea+1/(n1-Ea)+1/(m1-Ea)+1/(m0-(n1-Ea)))
    bd+=(a-Ea)**2/Va
gl=len(strata)-1
pbd=1-stats.chi2.cdf(bd,gl)
print("MH OR=%.4f | Breslow-Day chi2=%.2f gl=%d p=%.4f" % (or_mh,bd,gl,pbd))
print("(p<0.05 => OR heterogeneo entre categorias; reportar com cautela)")

# ---------- Roster-normalized rate excluding Nubank as a roster member ----------
print("\n=== ROSTER NORMALIZADO SEM NUBANK ===")
# fintech roster 19 -> 18 sem Nubank
fin=df[df.vertical=='fintech']
k_loo=int(fin['cited_loo'].sum()); n=len(fin)
print("fintech LOO rate=%.4f; rate/roster(18)=%.5f" % (k_loo/n, (k_loo/n)/18))
print("compare varejo rate/roster(15)=%.5f" % (0.2494/15))

# ---------- Share of Nubank within fintech entity mentions ----------
allmentions=[e for sub in fin['ents'] for e in sub]
from collections import Counter
cnt=Counter(x.lower() for x in allmentions)
total=sum(cnt.values())
nu=sum(v for k,v in cnt.items() if k in NUBANK)
print("\nNubank share of fintech entity mentions: %d/%d = %.2f%%" % (nu,total,100*nu/total))
print("DONE")
