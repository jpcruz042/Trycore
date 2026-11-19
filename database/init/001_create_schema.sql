CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    description TEXT,
    cut_off_date DATE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_project_name_not_empty CHECK (BTRIM(name) <> '')
);

CREATE TABLE IF NOT EXISTS activities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,
    bac NUMERIC(14, 2) NOT NULL,
    planned_progress NUMERIC(5, 2) NOT NULL,
    actual_progress NUMERIC(5, 2) NOT NULL,
    actual_cost NUMERIC(14, 2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_activity_name_not_empty CHECK (BTRIM(name) <> ''),
    CONSTRAINT chk_activity_bac_non_negative CHECK (bac >= 0),
    CONSTRAINT chk_activity_planned_progress_range CHECK (planned_progress BETWEEN 0 AND 100),
    CONSTRAINT chk_activity_actual_progress_range CHECK (actual_progress BETWEEN 0 AND 100),
    CONSTRAINT chk_activity_actual_cost_non_negative CHECK (actual_cost >= 0)
);

CREATE INDEX IF NOT EXISTS idx_activities_project_id ON activities(project_id);

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_projects_updated_at ON projects;
CREATE TRIGGER trg_projects_updated_at
BEFORE UPDATE ON projects
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_activities_updated_at ON activities;
CREATE TRIGGER trg_activities_updated_at
BEFORE UPDATE ON activities
FOR EACH ROW EXECUTE FUNCTION set_updated_at();
