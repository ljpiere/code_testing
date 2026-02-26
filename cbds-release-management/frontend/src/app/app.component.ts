import { CommonModule, DatePipe, JsonPipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';

import { ConnectorConfig, ServiceName } from './core/models/connector.models';
import { DeployRequest } from './core/models/deploy.models';
import { ConnectorService } from './core/services/connector.service';
import { DeployService } from './core/services/deploy.service';
import { JFrogService } from './core/services/jfrog.service';
import { ServiceNowService } from './core/services/servicenow.service';

type ViewMode = 'deploys' | 'connectors';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, JsonPipe, DatePipe],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly deployService = inject(DeployService);
  private readonly connectorService = inject(ConnectorService);
  private readonly jfrogService = inject(JFrogService);
  private readonly serviceNowService = inject(ServiceNowService);

  readonly viewMode = signal<ViewMode>('deploys');
  readonly loadingDeploys = signal(false);
  readonly loadingConnectors = signal(false);
  readonly submittingDeploy = signal(false);
  readonly connectorSaving = signal(false);

  deploys: DeployRequest[] = [];
  connectors: ConnectorConfig[] = [];
  selectedDeployId: number | null = null;
  selectedConnectorService: ServiceName = 'servicenow';

  deployMessage = '';
  connectorMessage = '';
  integrationMessage = '';

  readonly serviceOptions: ServiceName[] = [
    'servicenow',
    'jfrog',
    'jenkins',
    'jira',
    'confluence',
    'servicenow_db',
  ];

  readonly deployForm = this.fb.nonNullable.group({
    jira_ticket: '',
    project_name: '',
    module_name: '',
    op_code: '',
    environment: 'prod',
    pipeline_name: '',
    technical_description: '',
    impacted_jobs_csv: '',
    impacted_tables_csv: '',
    build_number: '',
    jfrog_artifact: '',
    change_description: '',
    impact_if_not_deployed: '',
    deploy_technical_steps: '',
    requested_by: '',
    internal_status: 'draft',
  });

  readonly connectorForm = this.fb.nonNullable.group({
    service_name: 'servicenow' as ServiceName,
    base_url: '',
    username: '',
    token: '',
    auth_type: 'basic',
    active: true,
    extras_json: '{}',
  });

  ngOnInit(): void {
    this.refreshDeploys();
    this.refreshConnectors();
  }

  get selectedDeploy(): DeployRequest | undefined {
    return this.deploys.find((d) => d.id === this.selectedDeployId);
  }

  setView(mode: ViewMode): void {
    this.viewMode.set(mode);
  }

  refreshDeploys(): void {
    this.loadingDeploys.set(true);
    this.deployService.list().subscribe({
      next: (res) => {
        this.deploys = res.items;
        if (!this.selectedDeployId && this.deploys.length > 0) {
          this.selectedDeployId = this.deploys[0].id;
        }
      },
      error: (err) => {
        this.deployMessage = this.extractError(err);
      },
      complete: () => this.loadingDeploys.set(false),
    });
  }

  refreshConnectors(): void {
    this.loadingConnectors.set(true);
    this.connectorService.list().subscribe({
      next: (rows) => {
        this.connectors = rows;
        this.loadConnectorIntoForm(this.selectedConnectorService);
      },
      error: (err) => {
        this.connectorMessage = this.extractError(err);
      },
      complete: () => this.loadingConnectors.set(false),
    });
  }

  createDeploy(): void {
    this.deployMessage = '';
    this.submittingDeploy.set(true);

    const form = this.deployForm.getRawValue();
    const payload = {
      jira_ticket: form.jira_ticket.trim(),
      project_name: form.project_name.trim(),
      module_name: form.module_name.trim() || null,
      op_code: form.op_code.trim(),
      environment: form.environment,
      pipeline_name: form.pipeline_name.trim() || null,
      technical_description: form.technical_description.trim(),
      impacted_jobs: this.parseCsv(form.impacted_jobs_csv),
      impacted_tables: this.parseCsv(form.impacted_tables_csv),
      build_number: form.build_number.trim() || null,
      jfrog_artifact: form.jfrog_artifact.trim() || null,
      change_description: form.change_description.trim(),
      impact_if_not_deployed: form.impact_if_not_deployed.trim(),
      deploy_technical_steps: form.deploy_technical_steps.trim(),
      requested_by: form.requested_by.trim() || null,
      internal_status: form.internal_status,
      metadata_json: {},
    };

    this.deployService.create(payload).subscribe({
      next: (created) => {
        this.deployMessage = `Deploy registrado (#${created.id})`;
        this.selectedDeployId = created.id;
        this.refreshDeploys();
      },
      error: (err) => {
        this.deployMessage = this.extractError(err);
      },
      complete: () => this.submittingDeploy.set(false),
    });
  }

  lookupJfrogArtifact(): void {
    const values = this.deployForm.getRawValue();
    if (!values.build_number.trim()) {
      this.integrationMessage = 'Ingresa build number para consultar JFrog.';
      return;
    }
    const buildName = values.module_name.trim() || values.project_name.trim();
    if (!buildName) {
      this.integrationMessage = 'Ingresa proyecto o módulo para usar como build_name.';
      return;
    }

    this.integrationMessage = 'Consultando JFrog...';
    this.jfrogService.lookupBuild({ build_name: buildName, build_number: values.build_number.trim() }).subscribe({
      next: (res) => {
        this.integrationMessage = res.ok
          ? `JFrog OK${res.artifact_path ? ` - Artifacto: ${res.artifact_path}` : ''}`
          : `JFrog error: ${res.detail ?? 'sin detalle'}`;
        if (res.artifact_path) {
          this.deployForm.patchValue({ jfrog_artifact: res.artifact_path });
        }
      },
      error: (err) => {
        this.integrationMessage = this.extractError(err);
      },
    });
  }

  createServiceNowChangeForSelected(): void {
    const deploy = this.deploys.find((d) => d.id === this.selectedDeployId);
    if (!deploy) {
      this.integrationMessage = 'Selecciona un deploy para crear CHG.';
      return;
    }

    this.integrationMessage = 'Creando CHG en ServiceNow...';
    this.serviceNowService
      .createChange({
        deploy_request_id: deploy.id,
        short_description: `[${deploy.project_name}] Deploy ${deploy.jira_ticket}`,
        description: [
          `Proyecto: ${deploy.project_name}`,
          `JIRA: ${deploy.jira_ticket}`,
          `OP: ${deploy.op_code}`,
          `Build: ${deploy.build_number ?? 'N/A'}`,
          `Artifacto: ${deploy.jfrog_artifact ?? 'N/A'}`,
          '',
          'Descripcion tecnica:',
          deploy.technical_description,
          '',
          'Descripcion del cambio:',
          deploy.change_description,
          '',
          'Impacto si no se realiza:',
          deploy.impact_if_not_deployed,
          '',
          'Pasos de deploy:',
          deploy.deploy_technical_steps,
        ].join('\n'),
        extra_fields: {},
      })
      .subscribe({
        next: (res) => {
          this.integrationMessage = res.ok
            ? `CHG creado: ${res.chg_number ?? 'sin numero'}`
            : `ServiceNow error: ${res.detail ?? 'sin detalle'}`;
          this.refreshDeploys();
        },
        error: (err) => {
          this.integrationMessage = this.extractError(err);
        },
      });
  }

  syncServiceNowStatus(deployId: number): void {
    this.integrationMessage = 'Sincronizando estado CHG...';
    this.serviceNowService.syncDeployStatus(deployId).subscribe({
      next: (res) => {
        this.integrationMessage = res.ok
          ? `CHG ${res.chg_number}: estado ${res.state ?? 'N/A'}`
          : `No se pudo sincronizar: ${res.detail ?? 'sin detalle'}`;
        this.refreshDeploys();
      },
      error: (err) => {
        this.integrationMessage = this.extractError(err);
      },
    });
  }

  selectConnector(serviceName: ServiceName): void {
    this.selectedConnectorService = serviceName;
    this.loadConnectorIntoForm(serviceName);
  }

  saveConnector(): void {
    let extras: Record<string, unknown> = {};
    const raw = this.connectorForm.getRawValue();
    try {
      extras = raw.extras_json.trim() ? (JSON.parse(raw.extras_json) as Record<string, unknown>) : {};
    } catch {
      this.connectorMessage = 'extras_json no es JSON valido.';
      return;
    }

    this.connectorSaving.set(true);
    this.connectorMessage = '';
    this.connectorService
      .upsert(raw.service_name, {
        service_name: raw.service_name,
        base_url: raw.base_url.trim() || null,
        username: raw.username.trim() || null,
        token: raw.token.trim() || undefined,
        auth_type: raw.auth_type as 'basic' | 'bearer' | 'api_key' | 'none',
        active: raw.active,
        extras,
      })
      .subscribe({
        next: (saved) => {
          this.connectorMessage = `Connector ${saved.service_name} guardado`;
          this.connectorForm.patchValue({ token: '' });
          this.refreshConnectors();
        },
        error: (err) => {
          this.connectorMessage = this.extractError(err);
        },
        complete: () => this.connectorSaving.set(false),
      });
  }

  testSelectedConnector(): void {
    const serviceName = this.connectorForm.getRawValue().service_name;
    this.connectorMessage = `Probando ${serviceName}...`;
    this.connectorService.test(serviceName).subscribe({
      next: (res) => {
        this.connectorMessage = `${res.ok ? 'OK' : 'ERROR'} - ${res.detail}`;
      },
      error: (err) => {
        this.connectorMessage = this.extractError(err);
      },
    });
  }

  trackByDeployId(_: number, item: DeployRequest): number {
    return item.id;
  }

  trackByService(_: number, item: ConnectorConfig): string {
    return item.service_name;
  }

  private loadConnectorIntoForm(serviceName: ServiceName): void {
    const connector = this.connectors.find((c) => c.service_name === serviceName);
    this.connectorForm.patchValue({
      service_name: serviceName,
      base_url: connector?.base_url ?? '',
      username: connector?.username ?? '',
      token: '',
      auth_type: connector?.auth_type ?? 'basic',
      active: connector?.active ?? true,
      extras_json: JSON.stringify(connector?.extras ?? {}, null, 2),
    });
  }

  private parseCsv(value: string): string[] {
    return value
      .split(',')
      .map((part) => part.trim())
      .filter(Boolean);
  }

  private extractError(error: unknown): string {
    if (typeof error === 'object' && error && 'error' in error) {
      const err = (error as { error?: unknown }).error;
      if (typeof err === 'string') return err;
      if (typeof err === 'object' && err && 'detail' in err) {
        const detail = (err as { detail?: unknown }).detail;
        if (typeof detail === 'string') return detail;
      }
    }
    return 'Ocurrio un error al procesar la solicitud.';
  }
}
