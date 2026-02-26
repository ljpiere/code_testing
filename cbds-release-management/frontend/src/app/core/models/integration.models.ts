export interface JFrogBuildLookupRequest {
  build_name: string;
  build_number: string;
}

export interface JFrogBuildLookupResponse {
  ok: boolean;
  build_name: string;
  build_number: string;
  artifact_path?: string | null;
  detail?: string | null;
  raw: Record<string, unknown>;
}

export interface ServiceNowChangeCreateRequest {
  deploy_request_id?: number | null;
  short_description: string;
  description: string;
  assignment_group?: string | null;
  category?: string | null;
  planned_start?: string | null;
  planned_end?: string | null;
  extra_fields: Record<string, unknown>;
}

export interface ServiceNowChangeResponse {
  ok: boolean;
  chg_number?: string | null;
  state?: string | null;
  detail?: string | null;
  raw: Record<string, unknown>;
}

