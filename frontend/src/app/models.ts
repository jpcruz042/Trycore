export interface Project {
  id: string;
  name: string;
  description?: string | null;
  cut_off_date?: string | null;
  created_at: string;
  updated_at: string;
}

export interface Activity {
  id: string;
  project_id: string;
  name: string;
  bac: string;
  planned_progress: string;
  actual_progress: string;
  actual_cost: string;
  pv?: string;
  ev?: string;
  cv?: string;
  sv?: string;
  cpi?: string | null;
  spi?: string | null;
  eac?: string | null;
  vac?: string | null;
  cpi_status?: string;
  spi_status?: string;
  created_at: string;
  updated_at: string;
}

export interface EvmIndicators {
  pv: string;
  ev: string;
  cv: string;
  sv: string;
  cpi: string | null;
  spi: string | null;
  eac: string | null;
  vac: string | null;
  cpi_status: string;
  spi_status: string;
}

export interface ActivityDraft {
  name: string;
  bac: number;
  planned_progress: number;
  actual_progress: number;
  actual_cost: number;
}

export interface ProjectEvm extends Project {
  indicators: EvmIndicators;
  activities: Activity[];
}
