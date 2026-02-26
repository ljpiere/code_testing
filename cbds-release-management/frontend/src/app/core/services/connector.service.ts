import { Injectable, inject } from '@angular/core';

import { ApiService } from './api.service';
import {
  ConnectorConfig,
  ConnectorTestResponse,
  ConnectorUpsertPayload,
  ServiceName,
} from '../models/connector.models';

@Injectable({ providedIn: 'root' })
export class ConnectorService {
  private readonly api = inject(ApiService);

  list() {
    return this.api.get<ConnectorConfig[]>('/connectors');
  }

  upsert(serviceName: ServiceName, payload: ConnectorUpsertPayload) {
    return this.api.put<ConnectorConfig>(`/connectors/${serviceName}`, payload);
  }

  test(serviceName: ServiceName) {
    return this.api.post<ConnectorTestResponse>('/connectors/test', { service_name: serviceName });
  }
}

