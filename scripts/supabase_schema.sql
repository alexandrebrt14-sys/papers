-- =============================================================
-- Schema Supabase para sync de dados do Papers
-- Criado para alimentar o dashboard em alexandrecaramaschi.com
-- =============================================================

-- papers_dashboard_data: dados agregados por vertical (citation rates, rankings, timeseries)
-- Atualizado diariamente pelo sync_to_supabase.py via GitHub Actions
CREATE TABLE IF NOT EXISTS papers_dashboard_data (
    vertical       TEXT PRIMARY KEY,
    citation_rates JSONB DEFAULT '[]'::jsonb,
    entity_rankings JSONB DEFAULT '[]'::jsonb,
    timeseries     JSONB DEFAULT '[]'::jsonb,
    collection_status JSONB DEFAULT '{}'::jsonb,
    kpis           JSONB DEFAULT '{}'::jsonb,
    updated_at     TIMESTAMPTZ DEFAULT now()
);

COMMENT ON TABLE papers_dashboard_data IS 'Dados agregados de citação por vertical, sincronizados do SQLite local via GitHub Actions';
COMMENT ON COLUMN papers_dashboard_data.citation_rates IS 'Array de {llm, total_queries, cited_count, citation_rate, avg_position}';
COMMENT ON COLUMN papers_dashboard_data.entity_rankings IS 'Top 15 entidades por contagem de citação: {entity, citation_count, citation_rate, top_llm}';
COMMENT ON COLUMN papers_dashboard_data.timeseries IS 'Série temporal diária dos últimos 90 dias: {date, rate, observations}';
COMMENT ON COLUMN papers_dashboard_data.collection_status IS '{last_run, total_runs_24h, modules: {module: status}}';
COMMENT ON COLUMN papers_dashboard_data.kpis IS '{total_observations, overall_rate, entities_monitored, days_collecting}';

-- papers_finops: controle de custos (linha única)
-- Atualizado diariamente pelo sync
CREATE TABLE IF NOT EXISTS papers_finops (
    id             TEXT PRIMARY KEY DEFAULT 'global',
    budget_monthly FLOAT DEFAULT 0,
    spent_monthly  FLOAT DEFAULT 0,
    pct_used       FLOAT DEFAULT 0,
    by_platform    JSONB DEFAULT '{}'::jsonb,
    updated_at     TIMESTAMPTZ DEFAULT now()
);

COMMENT ON TABLE papers_finops IS 'Resumo FinOps: orçamento mensal, gasto e breakdown por plataforma';

-- research_access_codes: códigos de verificação por email para acesso ao dashboard de pesquisa
CREATE TABLE IF NOT EXISTS research_access_codes (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email       TEXT NOT NULL,
    code        TEXT NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT now(),
    expires_at  TIMESTAMPTZ NOT NULL,
    used_at     TIMESTAMPTZ
);

COMMENT ON TABLE research_access_codes IS 'Códigos OTP para verificação de email no acesso ao dashboard de pesquisa';

CREATE INDEX IF NOT EXISTS idx_access_codes_email_expires
    ON research_access_codes (email, expires_at);

-- research_access_log: registro de acessos ao dashboard
CREATE TABLE IF NOT EXISTS research_access_log (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email       TEXT NOT NULL,
    accessed_at TIMESTAMPTZ DEFAULT now(),
    ip          TEXT,
    user_agent  TEXT
);

COMMENT ON TABLE research_access_log IS 'Log de acessos ao dashboard de pesquisa para auditoria';

-- =============================================================
-- Row Level Security (RLS)
-- =============================================================

ALTER TABLE papers_dashboard_data ENABLE ROW LEVEL SECURITY;
ALTER TABLE papers_finops ENABLE ROW LEVEL SECURITY;
ALTER TABLE research_access_codes ENABLE ROW LEVEL SECURITY;
ALTER TABLE research_access_log ENABLE ROW LEVEL SECURITY;

-- papers_dashboard_data: leitura pública (anon pode SELECT)
CREATE POLICY "papers_dashboard_data_select_anon"
    ON papers_dashboard_data FOR SELECT
    TO anon
    USING (true);

-- papers_finops: leitura pública
CREATE POLICY "papers_finops_select_anon"
    ON papers_finops FOR SELECT
    TO anon
    USING (true);

-- research_access_codes: anon pode inserir (gerar código) e consultar (verificar código)
CREATE POLICY "research_access_codes_insert_anon"
    ON research_access_codes FOR INSERT
    TO anon
    WITH CHECK (true);

CREATE POLICY "research_access_codes_select_anon"
    ON research_access_codes FOR SELECT
    TO anon
    USING (true);

-- research_access_log: anon pode apenas inserir (registrar acesso)
CREATE POLICY "research_access_log_insert_anon"
    ON research_access_log FOR INSERT
    TO anon
    WITH CHECK (true);
