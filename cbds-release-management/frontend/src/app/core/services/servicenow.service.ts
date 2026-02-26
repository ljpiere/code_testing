import { Injectable, inject } from '@angular/core';

import { ApiService } from './api.service';
import { ServiceNowChangeCreateRequest, ServiceNowChangeResponse } from '../models/integration.models';

@Injectable({ providedIn: 'root' })
export class ServiceNowService {
  private readonly api = inject(ApiService);

  createChange(payload: ServiceNowChangeCreateRequest) {
    return this.api.post<ServiceNowChangeResponse>('/servicenow/changes', payload);
  }

  syncDeployStatus(deployId: number) {
    return this.api.post<{ ok: boolean; chg_number: string; state?: string | null; detail?: string | null }>(
      `/servicenow/sync/deploy/${deployId}`,
      {}
    );
  }
}

