# code_testing
A miscellaneus for code

```
cbds-release-management/
├─ README.md
├─ docker-compose.yml                  # opcional (frontend + backend)
├─ .env                                # variables (backend)
├─ frontend/
│  ├─ angular.json
│  ├─ package.json
│  ├─ src/
│  │  ├─ environments/
│  │  │  ├─ environment.ts
│  │  │  └─ environment.prod.ts
│  │  ├─ app/
│  │  │  ├─ app.component.ts
│  │  │  ├─ app.component.html
│  │  │  ├─ app.component.scss
│  │  │  ├─ app.routes.ts
│  │  │  ├─ core/
│  │  │  │  ├─ guards/auth.guard.ts
│  │  │  │  ├─ interceptors/auth.interceptor.ts
│  │  │  │  ├─ models/
│  │  │  │  │  ├─ auth.models.ts
│  │  │  │  │  ├─ metrics.models.ts
│  │  │  │  │  ├─ jenkins.models.ts
│  │  │  │  │  ├─ confluence.models.ts
│  │  │  │  │  └─ servicenow.models.ts
│  │  │  │  └─ services/
│  │  │  │     ├─ api.service.ts
│  │  │  │     ├─ auth.service.ts
│  │  │  │     ├─ metrics.service.ts
│  │  │  │     ├─ jenkins.service.ts
│  │  │  │     ├─ confluence.service.ts
│  │  │  │     └─ servicenow.service.ts
│  │  │  ├─ layout/
│  │  │  │  ├─ shell.component.ts
│  │  │  │  ├─ shell.component.html
│  │  │  │  └─ shell.component.scss
│  │  │  ├─ shared/
│  │  │  │  ├─ components/
│  │  │  │  │  ├─ metric-card/
│  │  │  │  │  │  ├─ metric-card.component.ts
│  │  │  │  │  │  └─ metric-card.component.scss
│  │  │  │  └─ ui/material.imports.ts
│  │  │  ├─ features/
│  │  │  │  ├─ dashboard/dashboard.component.ts
│  │  │  │  ├─ dashboard/dashboard.component.html
│  │  │  │  ├─ dashboard/dashboard.component.scss
│  │  │  │  ├─ auth/login.component.ts
│  │  │  │  ├─ auth/login.component.html
│  │  │  │  ├─ auth/login.component.scss
│  │  │  │  ├─ jenkins/
│  │  │  │  │  ├─ trigger.component.ts
│  │  │  │  │  ├─ trigger.component.html
│  │  │  │  │  ├─ logs.component.ts
│  │  │  │  │  └─ logs.component.html
│  │  │  │  ├─ confluence/confluence-form.component.ts
│  │  │  │  ├─ confluence/confluence-form.component.html
│  │  │  │  ├─ servicenow/change-request.component.ts
│  │  │  │  └─ servicenow/change-request.component.html
│  │  │  └─ styles.scss
│  │  └─ assets/
│  └─ ...
└─ backend/
   ├─ pyproject.toml                   # o requirements.txt
   ├─ app/
   │  ├─ main.py
   │  ├─ core/
   │  │  ├─ config.py
   │  │  ├─ security.py
   │  │  └─ cors.py
   │  ├─ models/
   │  │  ├─ auth.py
   │  │  ├─ metrics.py
   │  │  ├─ jenkins.py
   │  │  ├─ confluence.py
   │  │  └─ servicenow.py
   │  ├─ routers/
   │  │  ├─ auth.py
   │  │  ├─ metrics.py
   │  │  ├─ jenkins.py
   │  │  ├─ confluence.py
   │  │  └─ servicenow.py
   │  └─ services/                     # integraciones futuras
   │     ├─ jenkins_client.py
   │     ├─ confluence_client.py
   │     └─ servicenow_client.py
   └─ ...

```

### Comandos de scaffolding (referencia)

```
# Angular
ng new frontend --routing --style=scss
cd frontend

# UI
ng add @angular/material

# (Opcional) chart.js para gráfica simple
npm i chart.js

```