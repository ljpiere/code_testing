# CBDS Release Management

Aplicacion para registrar solicitudes de deploy, asociar evidencias de build/artifactos (JFrog), manejar CHG de ServiceNow y parametrizar conectores (usuarios/tokens).

## Objetivo del MVP

- Capturar la informacion clave del deploy:
  - proyecto
  - JIRA
  - codigo OP
  - descripcion tecnica
  - jobs impactados
  - tablas impactadas
  - build number
  - descripcion del cambio
  - impacto de no realizar el cambio
  - descripcion tecnica del deploy
- Registrar y consultar solicitudes de deploy en backend Python (FastAPI + SQLite local).
- Parametrizar conectores (`servicenow`, `jfrog`, `jenkins`, `jira`, `confluence`, `servicenow_db`) con `base_url`, usuario, token y extras JSON.
- Consumir APIs para:
  - consultar build en JFrog
  - crear y consultar CHG en ServiceNow
  - disparar jobs de Jenkins

## Estructura

```text
cbds-release-management/
  backend/    # FastAPI
  frontend/   # Angular (standalone)
  docs/       # arquitectura / diagramas
```

## Diagramas de arquitectura

- Ver `cbds-release-management/docs/architecture-diagrams.md`
- Incluye:
  - grafico de componentes MVP
  - C4 C1 (Contexto)
  - C4 C2 (Contenedores)
  - C4 C3 (Componentes Backend)
  - C4 C3 (Componentes Frontend)

## Backend (Python / FastAPI)

### Endpoints principales

- `GET /health`
- `GET /api/deploys`
- `POST /api/deploys`
- `GET /api/deploys/{id}`
- `PATCH /api/deploys/{id}`
- `GET /api/connectors`
- `PUT /api/connectors/{service_name}`
- `POST /api/connectors/test`
- `POST /api/jfrog/builds/lookup`
- `GET /api/servicenow/changes/{chg_number}`
- `POST /api/servicenow/changes`
- `POST /api/servicenow/sync/deploy/{deploy_id}`
- `POST /api/jenkins/jobs/trigger`

### Ejecutar local

```powershell
cd cbds-release-management/backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Si prefieres `pyproject.toml`:

```powershell
pip install .
uvicorn app.main:app --reload
```

Nota: este repo incluye `pyproject.toml`. Si tu proceso interno exige Artifactory/JFrog, revisa la seccion de configuracion de `pip` mas abajo.

## Frontend (Angular)

### Pantallas MVP

- `Deploys`
  - formulario de captura de solicitud
  - lookup de artifacto en JFrog (por `build_name` + `build_number`)
  - lista de deploys
  - accion para crear CHG en ServiceNow
  - accion para sincronizar estado de CHG
- `Conectores`
  - administracion de URLs/usuarios/tokens (mascarando token en lectura)
  - prueba basica de conectividad por servicio

### Ejecutar local

```powershell
cd cbds-release-management/frontend
npm install
npm start
```

Si `npm` debe usar JFrog, revisa `.npmrc.example`.

## Parametrizacion de credenciales (usuarios y tokens)

El backend persiste configuracion de conectores en la tabla `connector_configs`.

- Campos parametrizables por servicio:
  - `base_url`
  - `username`
  - `token`
  - `auth_type`
  - `active`
  - `extras` (JSON libre para `repo`, `crumb`, headers, etc.)

Consideracion de seguridad:

- En este MVP el token se guarda en BD para permitir administracion desde UI.
- En ambiente productivo del banco se recomienda reemplazar almacenamiento del campo `token` por Vault/KMS/Secret Manager y solo guardar referencia.

## Integracion esperada con tu flujo

1. Usuario registra la solicitud de deploy con JIRA + datos tecnicos.
2. Se consulta/valida `build_number` en JFrog para recuperar artifacto.
3. Se crea (o asocia) CHG en ServiceNow usando la informacion del deploy.
4. Se sincroniza el estado del CHG para visibilidad operativa.
5. (Opcional) Se dispara job de Jenkins correspondiente (`dev`, `staging`, `prod`).

## Configuracion de pip con JFrog (Windows / Linux)

### Windows (`pip.ini`)

Usa `cbds-release-management/backend/pip.ini.example` como plantilla.

### Linux/Mac (`pip.conf`)

Usa `cbds-release-management/backend/pip.conf.example` como plantilla.

## Configuracion de npm con JFrog

Usa `cbds-release-management/frontend/.npmrc.example` como plantilla.

## Pendientes recomendados para la siguiente iteracion

- autenticacion/roles (SSO/LDAP/OAuth corporativo)
- auditoria de cambios (quien modifica CHG/conectores)
- cifrado de secretos
- integracion real con BD de ServiceNow (tabla SQL de CHG/status)
- reglas de validacion por modulo/pipeline
- templates de descripcion CHG por tipo de cambio
