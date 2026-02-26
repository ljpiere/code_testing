export interface DeployRequest {
  id: number;
  jira_ticket: string;
  project_name: string;
  module_name?: string | null;
  op_code: string;
  environment: string;
  pipeline_name?: string | null;
  technical_description: string;
  impacted_jobs: string[];
  impacted_tables: string[];
  build_number?: string | null;
  jfrog_artifact?: string | null;
  change_description: string;
  impact_if_not_deployed: string;
  deploy_technical_steps: string;
  requested_by?: string | null;
  servicenow_chg?: string | null;
  servicenow_status?: string | null;
  internal_status: string;
  metadata_json: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface DeployListResponse {
  items: DeployRequest[];
  total: number;
}

export interface DeployCreatePayload {
  jira_ticket: string;
  project_name: string;
  module_name?: string | null;
  op_code: string;
  environment: string;
  pipeline_name?: string | null;
  technical_description: string;
  impacted_jobs: string[];
  impacted_tables: string[];
  build_number?: string | null;
  jfrog_artifact?: string | null;
  change_description: string;
  impact_if_not_deployed: string;
  deploy_technical_steps: string;
  requested_by?: string | null;
  internal_status: string;
  metadata_json: Record<string, unknown>;
}

