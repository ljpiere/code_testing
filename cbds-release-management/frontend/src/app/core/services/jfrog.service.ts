import { Injectable, inject } from '@angular/core';

import { ApiService } from './api.service';
import { JFrogBuildLookupRequest, JFrogBuildLookupResponse } from '../models/integration.models';

@Injectable({ providedIn: 'root' })
export class JFrogService {
  private readonly api = inject(ApiService);

  lookupBuild(payload: JFrogBuildLookupRequest) {
    return this.api.post<JFrogBuildLookupResponse>('/jfrog/builds/lookup', payload);
  }
}

