-- Schema para tabelas Papers no Supabase
-- Executar no SQL Editor: supabase.com/dashboard/project/drzqkrqebvhcjotwhups/sql

-- Tabela principal: dados agregados por vertical (atualizada diariamente via sync)
CREATE TABLE IF NOT EXISTS papers_dashboard_data (
    id BIGSERIAL PRIMARY KEY,
    vertical TEXT NOT NULL UNIQUE,
    citation_rates JSONB DEFAULT '[]',
    entity_rankings JSONB DEFAULT '[]',
    timeseries JSONB DEFAULT '[]',
    collection_status JSONB DEFAULT '{}',
    kpis JSONB DEFAULT '{}',
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS but allow service_role full access
ALTER TABLE papers_dashboard_data ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Service role full access" ON papers_dashboard_data
    FOR ALL USING (true) WITH CHECK (true);

-- Tabela FinOps: resumo de gastos (atualizada diariamente)
CREATE TABLE IF NOT EXISTS papers_finops (
    id TEXT PRIMARY KEY DEFAULT 'global',
    budget_monthly NUMERIC DEFAULT 0,
    spent_monthly NUMERIC DEFAULT 0,
    pct_used NUMERIC DEFAULT 0,
    by_platform JSONB DEFAULT '{}',
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE papers_finops ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Service role full access" ON papers_finops
    FOR ALL USING (true) WITH CHECK (true);

-- Tabela de sessões de pesquisa (para autenticação do /research dashboard)
CREATE TABLE IF NOT EXISTS papers_research_sessions (
    id BIGSERIAL PRIMARY KEY,
    email TEXT NOT NULL,
    code TEXT NOT NULL,
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ DEFAULT NOW() + INTERVAL '10 minutes'
);

ALTER TABLE papers_research_sessions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Service role full access" ON papers_research_sessions
    FOR ALL USING (true) WITH CHECK (true);

-- Índices
CREATE INDEX IF NOT EXISTS idx_dashboard_vertical ON papers_dashboard_data(vertical);
CREATE INDEX IF NOT EXISTS idx_sessions_email ON papers_research_sessions(email);
CREATE INDEX IF NOT EXISTS idx_sessions_code ON papers_research_sessions(code);
