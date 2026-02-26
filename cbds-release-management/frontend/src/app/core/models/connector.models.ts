export type ServiceName =
  | 'confluence'
  | 'jenkins'
  | 'servicenow'
  | 'servicenow_db'
  | 'jfrog'
  | 'jira';

export type AuthType = 'basic' | 'bearer' | 'api_key' | 'none';

export interface ConnectorConfig {
  id: number;
  service_name: ServiceName;
  base_url?: string | null;
  username?: string | null;
  auth_type: AuthType;
  active: boolean;
  extras: Record<string, unknown>;
  token_masked?: string | null;
  created_at: string;
  updated_at: string;
}

export interface ConnectorUpsertPayload {
  service_name: ServiceName;
  base_url?: string | null;
  username?: string | null;
  token?: string | null;
  auth_type: AuthType;
  active: boolean;
  extras: Record<string, unknown>;
}

export interface ConnectorTestResponse {
  service_name: ServiceName;
  ok: boolean;
  detail: string;
}

