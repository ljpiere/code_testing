import { Injectable, inject } from '@angular/core';

import { ApiService } from './api.service';
import { DeployCreatePayload, DeployListResponse, DeployRequest } from '../models/deploy.models';

@Injectable({ providedIn: 'root' })
export class DeployService {
  private readonly api = inject(ApiService);

  list(params?: { q?: string; environment?: string; internal_status?: string }) {
    return this.api.get<DeployListResponse>('/deploys', params);
  }

  create(payload: DeployCreatePayload) {
    return this.api.post<DeployRequest>('/deploys', payload);
  }
}

