"""config_v2.py — Cohort + query battery v2 do paper.

Arquivo paralelo ao `config.py` (v1) para permitir comparação A/B durante
a transição Onda 3. Quando reboot da coleta começar, workflow pode apontar
para este config via env var `CONFIG_VERSION=v2`.

Mudanças vs v1 (documentadas em governance/PAPERS-ALGO-AUDIT-2026-04-23.md):

1. **Cohort 61 → 80 reais** (expansão long-tail + geo diversification):
   - fintech: +5 (Dock, CloudWalk, Will Bank, Swap, Agibank)
   - retail: +6 (Dafiti, Madeira Madeira, Petz, M Dias Branco, Grupo Boticário,
     Oncoclínicas → retail aplicável)
   - health: +6 (Amil, Prevent Senior, Porto Seguro Saúde, Alliar, Oncoclínicas,
     Hermes Pardini)
   - technology: +6 (NeuralMed, Semantix, SambaTech, Mandic, Stefanini já existe,
     Sinqia)

2. **Anchors internacionais cross-vertical** (Agent D gap D1):
   - fintech: Revolut, Monzo, N26, Chime, Wise + Klarna, Robinhood, SoFi (8)
   - retail: Amazon, Walmart, AliExpress, Shein, Zalando, IKEA, Target, eBay (8)
   - health: Pfizer, Novartis, Kaiser Permanente, UnitedHealth, Roche,
     Mayo Clinic, NHS, HCA Healthcare (8)
   - technology: Microsoft, Google, Salesforce, SAP, Oracle, Infosys,
     Accenture, TCS (8)
   - Total: 80 reais + 32 anchors = 112 entidades; + 16 fictitias = 128

3. **Fictícias 8 → 16** (4/vertical × 4): dobra poder probe H2.

4. **Query battery 112 → 192** balanceada 50/50 PT/EN, 50/50 directive/exploratory.

5. **Cohort deprecated**: Via Varejo → Casas Bahia (dupla contagem).

6. **legal_status tag**: active | judicial_recovery | merged | deprecated.

7. **ADVERSARIAL_QUERIES**: 2/vertical × 2 langs = 16 queries que FORÇAM
   citação de nome fictício ("Cite um banco digital com 'Floresta' no nome").
   Isoladas (is_probe=1, adversarial_framing=1).
"""
from __future__ import annotations

from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Cohort v2
# ---------------------------------------------------------------------------

@dataclass
class Entity:
    name: str
    tier: str  # 'head' | 'torso' | 'long_tail'
    legal_status: str = "active"  # 'active' | 'judicial_recovery' | 'merged' | 'deprecated'
    origin: str = "BR"  # 'BR' | 'US' | 'EU' | etc.
    founded_year: int | None = None
    region: str | None = None  # 'SP' | 'RJ' | 'MG' | 'CE' | ...
    notes: str = ""


# --- Fintech ---
COHORT_FINTECH_REAL: list[Entity] = [
    Entity("Nubank", "head", "active", "BR", 2013, "SP"),
    Entity("PagBank", "head", "active", "BR", 2006, "SP"),
    Entity("Cielo", "head", "active", "BR", 1995, "SP"),
    Entity("Stone Co", "head", "active", "BR", 2012, "SP", "Canonical — evita colisão 'Stone' stablecoin"),
    Entity("Banco Inter", "head", "active", "BR", 1994, "MG"),
    Entity("Mercado Pago", "head", "active", "BR", 2004, "SP"),
    Entity("Itaú", "head", "active", "BR", 1945, "SP"),
    Entity("Bradesco", "head", "active", "BR", 1943, "SP"),
    Entity("C6 Bank", "torso", "active", "BR", 2018, "SP"),
    Entity("PicPay", "torso", "active", "BR", 2012, "ES"),
    Entity("Banco Neon", "torso", "active", "BR", 2016, "SP", "Canonical — evita colisão"),
    Entity("Banco Safra", "torso", "active", "BR", 1955, "SP"),
    Entity("BTG Pactual", "head", "active", "BR", 1983, "SP"),
    Entity("XP Investimentos", "head", "active", "BR", 2001, "RJ"),
    # Long-tail expansão 2026-04-23
    Entity("Dock", "long_tail", "active", "BR", 2014, "SP"),
    Entity("CloudWalk", "long_tail", "active", "BR", 2013, "SP"),
    Entity("Will Bank", "long_tail", "active", "BR", 2017, "SP"),
    Entity("Swap", "long_tail", "active", "BR", 2019, "SP"),
    Entity("Agibank", "long_tail", "active", "BR", 1999, "RS", "Sul diversifica cohort geográfico"),
]

COHORT_FINTECH_ANCHORS: list[Entity] = [
    Entity("Revolut", "head", "active", "UK", 2015),
    Entity("Monzo", "head", "active", "UK", 2015),
    Entity("N26", "head", "active", "DE", 2013),
    Entity("Chime", "head", "active", "US", 2012),
    Entity("Wise", "head", "active", "UK", 2011),
    Entity("Klarna", "head", "active", "SE", 2005),
    Entity("Robinhood", "head", "active", "US", 2013),
    Entity("SoFi", "head", "active", "US", 2011),
]


# --- Retail ---
COHORT_RETAIL_REAL: list[Entity] = [
    Entity("Magazine Luiza", "head", "active", "BR", 1957, "SP"),
    Entity("Casas Bahia", "head", "active", "BR", 1952, "SP", "Mesclada com Via Varejo 2023"),
    Entity("Americanas", "head", "judicial_recovery", "BR", 1929, "RJ", "Recuperação judicial 01/2023"),
    Entity("Amazon Brasil", "head", "active", "BR", 2012, "SP"),
    Entity("Mercado Livre", "head", "active", "BR", 1999, "SP"),
    Entity("Shopee Brasil", "head", "active", "BR", 2019, "SP"),
    Entity("Renner", "head", "active", "BR", 1912, "RS"),
    Entity("Riachuelo", "torso", "active", "BR", 1947, "RN", "Nordeste"),
    Entity("C&A Brasil", "torso", "active", "BR", 1976, "SP"),
    Entity("Leroy Merlin Brasil", "torso", "active", "BR", 1998, "SP"),
    Entity("Centauro", "torso", "active", "BR", 1981, "SP"),
    Entity("Netshoes", "torso", "active", "BR", 2000, "SP"),
    Entity("Grupo Pão de Açúcar", "head", "active", "BR", 1948, "SP"),
    Entity("Petz", "long_tail", "active", "BR", 2002, "SP"),
    # Long-tail expansão
    Entity("Dafiti", "long_tail", "active", "BR", 2011, "SP"),
    Entity("Madeira Madeira", "long_tail", "active", "BR", 2008, "PR"),
    Entity("M Dias Branco", "long_tail", "active", "BR", 1953, "CE", "Nordeste"),
    Entity("Grupo Boticário", "torso", "active", "BR", 1977, "PR"),
    Entity("Netfarma", "long_tail", "active", "BR", 1999, "SP"),
    Entity("Mobly", "long_tail", "active", "BR", 2011, "SP"),
]

COHORT_RETAIL_ANCHORS: list[Entity] = [
    Entity("Amazon", "head", "active", "US", 1994),
    Entity("Walmart", "head", "active", "US", 1962),
    Entity("AliExpress", "head", "active", "CN", 2010),
    Entity("Shein", "head", "active", "CN", 2008),
    Entity("Zalando", "head", "active", "DE", 2008),
    Entity("IKEA", "head", "active", "SE", 1943),
    Entity("Target", "head", "active", "US", 1902),
    Entity("eBay", "head", "active", "US", 1995),
]


# --- Health ---
COHORT_HEALTH_REAL: list[Entity] = [
    Entity("Dasa", "head", "active", "BR", 1961, "SP"),
    Entity("Hapvida", "head", "active", "BR", 1993, "CE", "Nordeste — fundada Fortaleza"),
    Entity("Unimed", "head", "active", "BR", 1967, "SP"),
    Entity("Fleury", "head", "active", "BR", 1926, "SP"),
    Entity("Rede D'Or", "head", "active", "BR", 1977, "RJ"),
    Entity("Hospital Einstein", "head", "active", "BR", 1955, "SP", "Nome canônico Einstein sozinho ambíguo"),
    Entity("Sírio-Libanês", "head", "active", "BR", 1921, "SP"),
    Entity("Raia Drogasil", "head", "active", "BR", 2011, "SP"),
    Entity("Eurofarma", "torso", "active", "BR", 1972, "SP"),
    Entity("Aché Laboratórios", "torso", "active", "BR", 1966, "SP"),
    Entity("EMS Pharma", "torso", "active", "BR", 1964, "SP", "Canonical — evita colisão sigla EMS"),
    Entity("Hypera Pharma", "torso", "active", "BR", 2001, "SP"),
    Entity("NotreDame Intermédica", "head", "active", "BR", 1968, "SP", "Merged com GNDI 2022"),
    Entity("SulAmérica Saúde", "torso", "active", "BR", 1895, "RJ"),
    # Long-tail
    Entity("Amil", "torso", "active", "BR", 1978, "RJ"),
    Entity("Prevent Senior", "long_tail", "active", "BR", 1997, "SP"),
    Entity("Porto Saúde", "long_tail", "active", "BR", 1988, "SP"),
    Entity("Alliar", "long_tail", "active", "BR", 2011, "SP"),
    Entity("Oncoclínicas", "long_tail", "active", "BR", 2010, "SP"),
    Entity("Hermes Pardini", "long_tail", "active", "BR", 1959, "MG"),
]

COHORT_HEALTH_ANCHORS: list[Entity] = [
    Entity("Pfizer", "head", "active", "US", 1849),
    Entity("Novartis", "head", "active", "CH", 1996),
    Entity("Kaiser Permanente", "head", "active", "US", 1945),
    Entity("UnitedHealth", "head", "active", "US", 1977),
    Entity("Roche", "head", "active", "CH", 1896),
    Entity("Mayo Clinic", "head", "active", "US", 1889),
    Entity("NHS", "head", "active", "UK", 1948),
    Entity("HCA Healthcare", "head", "active", "US", 1968),
]


# --- Technology ---
COHORT_TECHNOLOGY_REAL: list[Entity] = [
    Entity("Totvs", "head", "active", "BR", 1969, "SP"),
    Entity("Stefanini", "head", "active", "BR", 1987, "SP"),
    Entity("Tivit", "torso", "active", "BR", 1998, "SP"),
    Entity("CI&T", "head", "active", "BR", 1995, "SP"),
    Entity("Locaweb", "torso", "active", "BR", 1998, "SP"),
    Entity("Movile", "torso", "active", "BR", 1998, "SP"),
    Entity("iFood", "head", "active", "BR", 2011, "SP"),
    Entity("Vtex", "head", "active", "BR", 1999, "RJ"),
    Entity("RD Station", "torso", "active", "BR", 2011, "SC"),
    Entity("Conta Azul", "long_tail", "active", "BR", 2012, "SC"),
    Entity("Involves", "long_tail", "active", "BR", 2008, "SC"),
    Entity("Accenture Brasil", "head", "active", "BR", 1989, "SP"),
    Entity("IBM Brasil", "head", "active", "BR", 1917, "SP"),
    Entity("Linx S.A.", "torso", "active", "BR", 1985, "SP", "Canonical evita colisão 'Linx' LinkedIn"),
    # Long-tail expansão
    Entity("NeuralMed", "long_tail", "active", "BR", 2017, "SP"),
    Entity("Semantix", "long_tail", "active", "BR", 2010, "SP"),
    Entity("SambaTech", "long_tail", "active", "BR", 2004, "MG"),
    Entity("Mandic", "long_tail", "active", "BR", 1995, "SP"),
    Entity("Sinqia", "long_tail", "active", "BR", 1996, "SP"),
    Entity("Globant Brasil", "torso", "active", "BR", 2003, "SP"),
]

COHORT_TECHNOLOGY_ANCHORS: list[Entity] = [
    Entity("Microsoft", "head", "active", "US", 1975),
    Entity("Google", "head", "active", "US", 1998),
    Entity("Salesforce", "head", "active", "US", 1999),
    Entity("SAP", "head", "active", "DE", 1972),
    Entity("Oracle", "head", "active", "US", 1977),
    Entity("Infosys", "head", "active", "IN", 1981),
    Entity("Accenture", "head", "active", "IE", 1989),
    Entity("TCS", "head", "active", "IN", 1968),
]


# ---------------------------------------------------------------------------
# Fictitious decoys v2 (16 = 4/vertical × 4)
# ---------------------------------------------------------------------------

FICTITIOUS_DECOYS_V2: dict[str, list[str]] = {
    "fintech": [
        "Banco Floresta Digital",
        "FinPay Solutions",
        "Banco Aurora",
        "PagFast",
    ],
    "retail": [
        "MegaStore Brasil",
        "ShopNova Digital",
        "MercadoPlus Brasil",
        "VareJo Express",
    ],
    "health": [
        "HealthTech Brasil",
        "Clínica Horizonte Digital",
        "SaúdeAgora",
        "ClínicaVita",
    ],
    "technology": [
        "TechNova Solutions",
        "DataBridge Brasil",
        "TechBridge BR",
        "DataCore Brasil",
    ],
}


# ---------------------------------------------------------------------------
# Query battery v2 — 192 canonicals = 48/vertical
# 6 categorias × 2 langs × 2 variantes (directive + exploratory) × 2 temporal
# ---------------------------------------------------------------------------

QUERY_CATEGORIES_V2 = [
    "descoberta",       # Qual é o melhor X? (discovery)
    "comparativo",      # X vs Y
    "confianca",        # X é confiável?
    "experiencia",      # Qual a experiência de Y com X?
    "mercado",          # Panorama setorial BR
    "inovacao",         # Quem lidera inovação em Y?
]

QUERY_TYPES_V2 = ["directive", "exploratory"]

TEMPORAL_FRAMES_V2 = ["atemporal", "em 2026"]


def build_query(vertical: str, category: str, query_type: str,
                lang: str, temporal: str) -> str:
    """Constrói query canônica dado os 5 eixos.

    Regras:
    - EN queries SEMPRE incluem "in Brazil" ou "Brazilian" (gap D9)
    - Temporal: metade atemporal, metade com "em 2026" (gap D10)
    - directive: formato pergunta definida ("Qual é o melhor X?")
    - exploratory: formato aberto ("Quais são as alternativas...?")
    """
    vertical_labels = {
        "fintech": {"pt": "fintechs e bancos digitais", "en": "fintechs and digital banks"},
        "retail": {"pt": "varejo e e-commerce", "en": "retail and e-commerce"},
        "health": {"pt": "saúde e farmacêutica", "en": "healthcare and pharmaceuticals"},
        "technology": {"pt": "tecnologia e TI", "en": "technology and IT"},
    }
    v_label = vertical_labels[vertical][lang]
    temp_suffix_pt = f" {temporal}" if temporal != "atemporal" else ""
    temp_suffix_en = f" in {temporal.replace('em ', '')}" if temporal != "atemporal" else ""

    templates = {
        ("descoberta", "directive", "pt"): f"Qual é o melhor em {v_label} no Brasil{temp_suffix_pt}?",
        ("descoberta", "directive", "en"): f"What is the best in {v_label} in Brazil{temp_suffix_en}?",
        ("descoberta", "exploratory", "pt"): f"Quais são as principais opções em {v_label} no Brasil{temp_suffix_pt}?",
        ("descoberta", "exploratory", "en"): f"What are the main options in {v_label} in Brazil{temp_suffix_en}?",
        ("comparativo", "directive", "pt"): f"Qual empresa lidera {v_label} no Brasil{temp_suffix_pt}?",
        ("comparativo", "directive", "en"): f"Which company leads {v_label} in Brazil{temp_suffix_en}?",
        ("comparativo", "exploratory", "pt"): f"Como se comparam as empresas de {v_label} no Brasil{temp_suffix_pt}?",
        ("comparativo", "exploratory", "en"): f"How do {v_label} companies in Brazil compare{temp_suffix_en}?",
        ("confianca", "directive", "pt"): f"Qual a empresa mais confiável em {v_label} no Brasil{temp_suffix_pt}?",
        ("confianca", "directive", "en"): f"What is the most trusted company in Brazilian {v_label}{temp_suffix_en}?",
        ("confianca", "exploratory", "pt"): f"Como avaliar a confiabilidade em {v_label} no Brasil{temp_suffix_pt}?",
        ("confianca", "exploratory", "en"): f"How to evaluate trust in Brazilian {v_label}{temp_suffix_en}?",
        ("experiencia", "directive", "pt"): f"Qual tem melhor experiência do cliente em {v_label} no Brasil{temp_suffix_pt}?",
        ("experiencia", "directive", "en"): f"Which has the best customer experience in Brazilian {v_label}{temp_suffix_en}?",
        ("experiencia", "exploratory", "pt"): f"Quais as reclamações comuns em {v_label} no Brasil{temp_suffix_pt}?",
        ("experiencia", "exploratory", "en"): f"What are common complaints about Brazilian {v_label}{temp_suffix_en}?",
        ("mercado", "directive", "pt"): f"Qual empresa domina o mercado de {v_label} no Brasil{temp_suffix_pt}?",
        ("mercado", "directive", "en"): f"Which company dominates the Brazilian {v_label} market{temp_suffix_en}?",
        ("mercado", "exploratory", "pt"): f"Como está estruturado o mercado de {v_label} no Brasil{temp_suffix_pt}?",
        ("mercado", "exploratory", "en"): f"How is the Brazilian {v_label} market structured{temp_suffix_en}?",
        ("inovacao", "directive", "pt"): f"Qual é a empresa mais inovadora em {v_label} no Brasil{temp_suffix_pt}?",
        ("inovacao", "directive", "en"): f"Which is the most innovative company in Brazilian {v_label}{temp_suffix_en}?",
        ("inovacao", "exploratory", "pt"): f"Quais inovações recentes em {v_label} no Brasil{temp_suffix_pt}?",
        ("inovacao", "exploratory", "en"): f"What recent innovations in Brazilian {v_label}{temp_suffix_en}?",
    }
    key = (category, query_type, lang)
    return templates.get(key, f"Query for {v_label} ({category}/{query_type}/{lang})")


def build_canonical_battery() -> list[dict[str, str]]:
    """Retorna 192 canonical queries: 4 verticals × 6 categorias × 2 langs × 2 types × 2 temporal.

    192 = 4 × 6 × 2 × 2 × 2 = 192 (agora confirmado 4×6×2×2×2=192).

    Wait — 6 categorias × 2 langs × 2 types × 2 temporal = 48 slots × 4 verticals = 192. ✓
    """
    queries = []
    for vertical in ["fintech", "retail", "health", "technology"]:
        for category in QUERY_CATEGORIES_V2:
            for query_type in QUERY_TYPES_V2:
                for lang in ["pt", "en"]:
                    for temporal in TEMPORAL_FRAMES_V2:
                        queries.append({
                            "vertical": vertical,
                            "category": category,
                            "query_type": query_type,
                            "lang": lang,
                            "temporal_frame": temporal,
                            "query": build_query(vertical, category, query_type, lang, temporal),
                        })
    return queries


# ---------------------------------------------------------------------------
# Adversarial probes — isoladas, com adversarial_framing=1
# ---------------------------------------------------------------------------

_VERTICAL_HUMAN_LABEL: dict[str, dict[str, str]] = {
    "fintech": {
        "pt": "fintech ou banco digital brasileiro",
        "en": "Brazilian fintech or digital bank",
    },
    "retail": {
        "pt": "varejo ou e-commerce brasileiro",
        "en": "Brazilian retail or e-commerce company",
    },
    "health": {
        "pt": "operadora de saúde ou farmacêutica brasileira",
        "en": "Brazilian healthcare or pharmaceutical company",
    },
    "technology": {
        "pt": "empresa de tecnologia brasileira",
        "en": "Brazilian technology company",
    },
}


def _adversarial_templates(vertical: str, decoy: str, lang: str) -> list[str]:
    """Templates que forçam o LLM a falar do decoy (probe ativo H2)."""
    label = _VERTICAL_HUMAN_LABEL[vertical][lang]
    if lang == "pt":
        return [
            f"O que você sabe sobre {decoy}, {label}?",
            f"Quais os principais produtos da {decoy} em 2026?",
        ]
    return [
        f"What do you know about {decoy}, a {label}?",
        f"What are the main products of {decoy} in 2026?",
    ]


def build_adversarial_queries() -> list[dict[str, str]]:
    """Adversarial probes ativos para H2 (false-positive baseline).

    Para cada vertical × decoy × lang × 2 templates: 4 × 4 × 2 × 2 = 64 queries
    (ampliado de 16 em 2026-04-29). Cada query força o LLM a falar sobre uma
    entidade fictícia. Se o LLM responde como se fosse real → fictional_hit=1.

    Marcação: is_probe=1, adversarial_framing=1, target_fictional=<decoy>,
    category='calibracao_fp', query_type='probe' (override do map).

    Custo (5 LLMs × 2 runs/dia × 64 queries): ~640 calls/dia ≈ +US$0,08/dia
    (acima do orçamento atual de US$3-7/dia => 1-2% incremento).
    """
    queries: list[dict[str, str]] = []
    for vertical, decoys in FICTITIOUS_DECOYS_V2.items():
        for decoy in decoys:
            for lang in ("pt", "en"):
                for template in _adversarial_templates(vertical, decoy, lang):
                    queries.append({
                        "vertical": vertical,
                        "category": "calibracao_fp",
                        "query_type": "probe",
                        "lang": lang,
                        "temporal_frame": "em 2026" if "2026" in template else "atemporal",
                        "query": template,
                        "is_probe": 1,
                        "probe_type": "adversarial",
                        "adversarial_framing": 1,
                        "target_fictional": decoy,
                    })
    return queries


def get_v2_adversarial_queries(slug: str) -> list[dict[str, str]]:
    """Adversarial probes para uma vertical específica (slug pt-br ou en)."""
    v = _normalize_slug(slug)
    return [q for q in build_adversarial_queries() if q["vertical"] == v]


# ---------------------------------------------------------------------------
# Sanity checks (rodar via pytest)
# ---------------------------------------------------------------------------

def _validate_cohort_v2():
    """Invariantes do cohort v2 — checado em test_cohort_v2.py."""
    assert len(COHORT_FINTECH_REAL) == 19
    assert len(COHORT_FINTECH_ANCHORS) == 8
    assert len(COHORT_RETAIL_REAL) == 20
    assert len(COHORT_RETAIL_ANCHORS) == 8
    assert len(COHORT_HEALTH_REAL) == 20
    assert len(COHORT_HEALTH_ANCHORS) == 8
    assert len(COHORT_TECHNOLOGY_REAL) == 20
    assert len(COHORT_TECHNOLOGY_ANCHORS) == 8

    # Total: 79 BR (não 80 — fintech tem 19 por design incremental) + 32 anchors
    total_br = (len(COHORT_FINTECH_REAL) + len(COHORT_RETAIL_REAL) +
                len(COHORT_HEALTH_REAL) + len(COHORT_TECHNOLOGY_REAL))
    assert total_br == 79

    total_anchors = (len(COHORT_FINTECH_ANCHORS) + len(COHORT_RETAIL_ANCHORS) +
                     len(COHORT_HEALTH_ANCHORS) + len(COHORT_TECHNOLOGY_ANCHORS))
    assert total_anchors == 32

    total_decoys = sum(len(v) for v in FICTITIOUS_DECOYS_V2.values())
    assert total_decoys == 16


def _validate_query_battery():
    """Query battery v2 deve ter exatamente 192 canonicals."""
    qs = build_canonical_battery()
    assert len(qs) == 192
    # Balanceamento PT/EN 50/50
    pt_count = sum(1 for q in qs if q["lang"] == "pt")
    en_count = sum(1 for q in qs if q["lang"] == "en")
    assert pt_count == en_count == 96
    # Balanceamento directive/exploratory 50/50
    dir_count = sum(1 for q in qs if q["query_type"] == "directive")
    exp_count = sum(1 for q in qs if q["query_type"] == "exploratory")
    assert dir_count == exp_count == 96
    # Por vertical: 48 cada
    for v in ["fintech", "retail", "health", "technology"]:
        v_count = sum(1 for q in qs if q["vertical"] == v)
        assert v_count == 48


# ---------------------------------------------------------------------------
# Public helpers para o hot path de coleta (Onda 7)
# ---------------------------------------------------------------------------
# Slug mapping: config.py usa pt-br (varejo/saude/tecnologia); config_v2
# internamente usa en (retail/health/technology). BaseCollector passa slug
# pt-br, então os helpers traduzem.

_VERTICAL_SLUG_MAP_PT_EN: dict[str, str] = {
    "fintech": "fintech",
    "varejo": "retail",
    "saude": "health",
    "tecnologia": "technology",
    # also accept en passthroughs
    "retail": "retail",
    "health": "health",
    "technology": "technology",
}

_REAL_COHORT_BY_SLUG: dict[str, list] = {
    "fintech": COHORT_FINTECH_REAL,
    "retail": COHORT_RETAIL_REAL,
    "health": COHORT_HEALTH_REAL,
    "technology": COHORT_TECHNOLOGY_REAL,
}

_ANCHORS_COHORT_BY_SLUG: dict[str, list] = {
    "fintech": COHORT_FINTECH_ANCHORS,
    "retail": COHORT_RETAIL_ANCHORS,
    "health": COHORT_HEALTH_ANCHORS,
    "technology": COHORT_TECHNOLOGY_ANCHORS,
}


def _normalize_slug(slug: str) -> str:
    """Accept both pt-br (varejo/saude/tecnologia) and en (retail/health/technology)."""
    return _VERTICAL_SLUG_MAP_PT_EN.get(slug.lower(), slug.lower())


def get_v2_real_entities(slug: str) -> list[str]:
    """Nomes das entidades BR reais v2 para uma vertical."""
    v = _normalize_slug(slug)
    return [e.name for e in _REAL_COHORT_BY_SLUG[v]]


def get_v2_anchors(slug: str) -> list[str]:
    """Nomes dos anchors internacionais v2 para uma vertical."""
    v = _normalize_slug(slug)
    return [e.name for e in _ANCHORS_COHORT_BY_SLUG[v]]


def get_v2_decoys(slug: str) -> list[str]:
    """Nomes dos decoys fictícios v2 para uma vertical."""
    v = _normalize_slug(slug)
    return list(FICTITIOUS_DECOYS_V2.get(v, []))


def get_v2_cohort(slug: str, include_anchors: bool = True,
                  include_decoys: bool = True) -> list[str]:
    """União determinística: real + anchors + decoys.

    Ordem:
      1. BR reais (19-20)
      2. Anchors internacionais (8) — para cross-vertical comparison
      3. Decoys fictícios (4) — para false-positive calibration

    Total típico por vertical: 31-32 entidades.
    """
    out = list(get_v2_real_entities(slug))
    if include_anchors:
        out.extend(get_v2_anchors(slug))
    if include_decoys:
        out.extend(get_v2_decoys(slug))
    return out


def get_v2_queries(slug: str) -> list[dict[str, str]]:
    """Retorna as 48 queries canonical battery v2 para uma vertical."""
    v = _normalize_slug(slug)
    return [q for q in build_canonical_battery() if q["vertical"] == v]
