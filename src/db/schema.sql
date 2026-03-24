-- Papers Research Database Schema
-- Supports both SQLite (local) and Supabase (production)
-- All timestamps in UTC ISO 8601

-- ============================================================
-- Module 1: Multi-LLM Citation Tracker
-- ============================================================
CREATE TABLE IF NOT EXISTS citations (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp       TEXT NOT NULL,               -- ISO 8601 UTC
    llm             TEXT NOT NULL,               -- ChatGPT, Claude, Gemini, Perplexity, Copilot
    model           TEXT NOT NULL,               -- gpt-4o, claude-sonnet-4-20250514, etc.
    query           TEXT NOT NULL,
    query_category  TEXT NOT NULL,               -- brand, entity, concept, technical, b2a, market, academic
    query_lang      TEXT NOT NULL DEFAULT 'en',  -- en, pt
    cited           BOOLEAN NOT NULL DEFAULT 0,
    cited_entity    BOOLEAN DEFAULT 0,
    cited_domain    BOOLEAN DEFAULT 0,
    cited_person    BOOLEAN DEFAULT 0,
    position        INTEGER,                     -- 1=first third, 2=middle, 3=last third
    attribution     TEXT DEFAULT 'none',         -- linked, named, paraphrased, none
    source_count    INTEGER DEFAULT 0,
    our_source_count INTEGER DEFAULT 0,
    hedging_detected BOOLEAN DEFAULT 0,
    response_length INTEGER,
    response_text   TEXT,
    sources_json    TEXT,                        -- JSON array of source URLs
    latency_ms      INTEGER,
    token_count     INTEGER,
    created_at      TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_citations_timestamp ON citations(timestamp);
CREATE INDEX IF NOT EXISTS idx_citations_llm ON citations(llm);
CREATE INDEX IF NOT EXISTS idx_citations_query_category ON citations(query_category);
CREATE INDEX IF NOT EXISTS idx_citations_cited ON citations(cited);

-- ============================================================
-- Module 2: Competitor Benchmark Dataset
-- ============================================================
CREATE TABLE IF NOT EXISTS competitor_citations (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp       TEXT NOT NULL,
    llm             TEXT NOT NULL,
    model           TEXT NOT NULL,
    query           TEXT NOT NULL,
    query_category  TEXT NOT NULL,
    query_lang      TEXT NOT NULL DEFAULT 'en',
    entity          TEXT NOT NULL,               -- Competitor name or primary entity
    entity_type     TEXT NOT NULL,               -- 'primary' or 'competitor'
    cited           BOOLEAN NOT NULL DEFAULT 0,
    position        INTEGER,
    response_length INTEGER,
    created_at      TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_comp_entity ON competitor_citations(entity);
CREATE INDEX IF NOT EXISTS idx_comp_timestamp ON competitor_citations(timestamp);

-- ============================================================
-- Module 3: SERP vs AI Overlap Tracker
-- ============================================================
CREATE TABLE IF NOT EXISTS serp_ai_overlap (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp       TEXT NOT NULL,
    llm             TEXT NOT NULL,
    model           TEXT NOT NULL,
    query           TEXT NOT NULL,
    query_category  TEXT NOT NULL,
    serp_domain_count   INTEGER,
    ai_domain_count     INTEGER,
    overlap_count       INTEGER,
    overlap_pct         REAL,
    serp_only_count     INTEGER,
    ai_only_count       INTEGER,
    overlap_domains     TEXT,                    -- JSON array
    serp_only_domains   TEXT,                    -- JSON array
    ai_only_domains     TEXT,                    -- JSON array
    primary_in_serp     BOOLEAN DEFAULT 0,
    primary_in_ai       BOOLEAN DEFAULT 0,
    created_at          TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_overlap_timestamp ON serp_ai_overlap(timestamp);

-- ============================================================
-- Module 4: Content Intervention Tracker
-- ============================================================
CREATE TABLE IF NOT EXISTS interventions (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    slug                TEXT NOT NULL UNIQUE,
    intervention_type   TEXT NOT NULL,           -- schema_org, llms_txt, academic_citations, etc.
    description         TEXT NOT NULL,
    url                 TEXT NOT NULL,
    queries_json        TEXT NOT NULL,           -- JSON array of queries to monitor
    baseline_json       TEXT,                    -- JSON: {llm: cited_bool} before intervention
    registered_at       TEXT NOT NULL,
    status              TEXT DEFAULT 'active',   -- active, completed, cancelled
    created_at          TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS intervention_measurements (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    intervention_slug       TEXT NOT NULL REFERENCES interventions(slug),
    timestamp               TEXT NOT NULL,
    days_since_intervention INTEGER NOT NULL,
    citations_json          TEXT NOT NULL,       -- JSON: {llm: cited_bool}
    citation_rate           REAL,
    delta_from_baseline     REAL,
    details_json            TEXT,
    created_at              TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_measurements_slug ON intervention_measurements(intervention_slug);

-- ============================================================
-- Module 5: Time Series Persistence
-- ============================================================
CREATE TABLE IF NOT EXISTS daily_snapshots (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    date        TEXT NOT NULL UNIQUE,            -- YYYY-MM-DD
    module      TEXT NOT NULL,
    data_json   TEXT NOT NULL,                   -- Full snapshot as JSON
    created_at  TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_snapshots_date ON daily_snapshots(date);
CREATE INDEX IF NOT EXISTS idx_snapshots_module ON daily_snapshots(module);

-- ============================================================
-- Module 7: Citation Context Analysis
-- ============================================================
CREATE TABLE IF NOT EXISTS citation_context (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    citation_id     INTEGER REFERENCES citations(id),
    entity          TEXT NOT NULL,
    sentiment       TEXT,                        -- positive, neutral, negative
    attribution     TEXT,                        -- linked, named, paraphrased, none
    factual_accuracy_json TEXT,                  -- JSON with accuracy details
    position_tercile INTEGER,                    -- 1, 2, 3
    hedging         BOOLEAN DEFAULT 0,
    hedging_phrases TEXT,                        -- JSON array
    context_window  TEXT,                        -- 200-char window around mention
    sentiment_signals TEXT,                      -- JSON array
    created_at      TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_context_entity ON citation_context(entity);
CREATE INDEX IF NOT EXISTS idx_context_sentiment ON citation_context(sentiment);

-- ============================================================
-- Metadata
-- ============================================================
CREATE TABLE IF NOT EXISTS collection_runs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp   TEXT NOT NULL,
    module      TEXT NOT NULL,
    records     INTEGER NOT NULL DEFAULT 0,
    duration_ms INTEGER,
    status      TEXT DEFAULT 'success',         -- success, error, partial
    error_msg   TEXT,
    created_at  TEXT DEFAULT (datetime('now'))
);
