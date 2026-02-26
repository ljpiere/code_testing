# Diagramas de Arquitectura (MVP)

Este documento incluye:

- Grafico de componentes del MVP (interaccion funcional)
- Diagramas tipo C4:
  - C1 Contexto
  - C2 Contenedores
  - C3 Componentes (Backend)
  - C3 Componentes (Frontend)

## 1) Grafico de Componentes MVP (interaccion)

```mermaid
flowchart LR
    U[Analista / Release Manager]

    subgraph FE[Frontend Angular]
        UI[AppComponent UI\nDeploys + Conectores]
        DFS[DeployService]
        CFS[ConnectorService]
        JFS[JFrogService]
        SNS[ServiceNowService]
        AFS[ApiService]
        UI --> DFS
        UI --> CFS
        UI --> JFS
        UI --> SNS
        DFS --> AFS
        CFS --> AFS
        JFS --> AFS
        SNS --> AFS
    end

    subgraph BE[Backend FastAPI]
        API[FastAPI app/main.py]
        DR[Router Deploys]
        CR[Router Connectors]
        SR[Router ServiceNow]
        JR[Router JFrog]
        JKR[Router Jenkins]

        DModel[(DeployRequest)]
        CModel[(ConnectorConfig)]

        SVC1[Connector Service]
        SVC2[ServiceNow Client]
        SVC3[JFrog Client]
        SVC4[Jenkins Client]
        DB[(SQLite / SQLAlchemy)]

        API --> DR
        API --> CR
        API --> SR
        API --> JR
        API --> JKR

        DR --> DModel
        DR --> DB

        CR --> SVC1
        SVC1 --> CModel
        SVC1 --> DB

        SR --> SVC1
        SR --> SVC2
        SR --> DModel
        SR --> DB

        JR --> SVC1
        JR --> SVC3

        JKR --> SVC1
        JKR --> SVC4
    end

    subgraph EXT[Sistemas Externos]
        SN[ServiceNow API]
        JF[JFrog / Artifactory API]
        JK[Jenkins / CloudBees API]
        JI[JIRA (futuro)]
        CF[Confluence (futuro)]
        SDB[(BD ServiceNow / CHG Status\nfuturo)]
    end

    U --> UI
    AFS --> API
    SVC2 --> SN
    SVC3 --> JF
    SVC4 --> JK
    CR -. parametrizacion .-> JI
    CR -. parametrizacion .-> CF
    CR -. parametrizacion .-> SDB
```

## 2) C4 - C1 Contexto (System Context)

```mermaid
flowchart TB
    User[Usuario de Release / Soporte]
    System[CBDS Release Management\nSistema para registro y control de deploys]

    SN[ServiceNow]
    JF[JFrog / Artifactory]
    JK[Jenkins / CloudBees SDA]
    JIRA[JIRA]
    CONF[Confluence]
    SNDB[(BD de seguimiento CHG/STATUS)]

    User -->|Registra solicitudes, consulta estados,\ncrea CHG y prepara deploy| System
    System -->|Crea/consulta cambios (CHG)| SN
    System -->|Consulta builds y artefactos| JF
    System -->|Dispara jobs / consulta pipelines| JK
    System -.->|Valida referencia de ticket| JIRA
    System -.->|Documentacion / evidencias| CONF
    System -.->|Persistencia de CHG/STATUS corporativa| SNDB
```

## 3) C4 - C2 Contenedores (Container Diagram)

```mermaid
flowchart LR
    User[Usuario]

    subgraph System[CBDS Release Management]
        FE[Frontend Angular SPA\nCaptura de deploys + gestion de conectores]
        BE[Backend FastAPI\nAPI REST + reglas de negocio + integraciones]
        DB[(SQLite MVP / SQL corporativa futura)\nDeploys + Connectors]
    end

    SN[ServiceNow API]
    JF[JFrog API]
    JK[Jenkins/CloudBees API]
    JIRA[JIRA API (futuro)]
    CONF[Confluence API (futuro)]
    SNDB[(BD ServiceNow CHG/STATUS - futura)]

    User -->|HTTPS| FE
    FE -->|REST/JSON| BE
    BE -->|ORM / SQLAlchemy| DB
    BE -->|REST API| SN
    BE -->|REST API| JF
    BE -->|REST API| JK
    BE -.->|REST API| JIRA
    BE -.->|REST API| CONF
    BE -.->|SQL / driver corporativo| SNDB
```

## 4) C4 - C3 Componentes (Backend FastAPI)

```mermaid
flowchart TB
    subgraph FastAPI[Backend FastAPI]
        Main[main.py\nBootstrap + routers + startup]
        Config[core/config.py\nSettings (.env)]
        DBLayer[db.py\nEngine + Session]

        DeployRouter[routers/deploys.py]
        ConnectorsRouter[routers/connectors.py]
        ServiceNowRouter[routers/servicenow.py]
        JFrogRouter[routers/jfrog.py]
        JenkinsRouter[routers/jenkins.py]

        Schemas[Schemas Pydantic\n(deploys, connectors, integrations)]
        ConnectorSvc[services/connector_service.py]
        SNClient[services/servicenow_client.py]
        JFClient[services/jfrog_client.py]
        JKClient[services/jenkins_client.py]

        DeployModel[(models/DeployRequest)]
        ConnectorModel[(models/ConnectorConfig)]
    end

    SQL[(SQLite MVP / SQL futuro)]
    SN[ServiceNow API]
    JF[JFrog API]
    JK[Jenkins API]

    Main --> Config
    Main --> DBLayer
    Main --> DeployRouter
    Main --> ConnectorsRouter
    Main --> ServiceNowRouter
    Main --> JFrogRouter
    Main --> JenkinsRouter

    DeployRouter --> Schemas
    DeployRouter --> DeployModel
    DeployRouter --> DBLayer
    DBLayer --> SQL

    ConnectorsRouter --> Schemas
    ConnectorsRouter --> ConnectorSvc
    ConnectorSvc --> ConnectorModel
    ConnectorSvc --> DBLayer

    ServiceNowRouter --> Schemas
    ServiceNowRouter --> ConnectorSvc
    ServiceNowRouter --> SNClient
    ServiceNowRouter --> DeployModel
    ServiceNowRouter --> DBLayer
    SNClient --> SN

    JFrogRouter --> Schemas
    JFrogRouter --> ConnectorSvc
    JFrogRouter --> JFClient
    JFClient --> JF

    JenkinsRouter --> Schemas
    JenkinsRouter --> ConnectorSvc
    JenkinsRouter --> JKClient
    JKClient --> JK
```

## 5) C4 - C3 Componentes (Frontend Angular)

```mermaid
flowchart TB
    User[Usuario]

    subgraph Angular[Frontend Angular SPA]
        App[AppComponent\nUI principal]
        AppRoutes[app.routes.ts]
        Models[Modelos TS\n(deploy, connector, integration)]
        ApiSvc[ApiService]
        DeploySvc[DeployService]
        ConnectorSvc[ConnectorService]
        JFrogSvc[JFrogService]
        ServiceNowSvc[ServiceNowService]
        Env[environment.ts]
    end

    API[Backend FastAPI /api]

    User --> App
    App --> AppRoutes
    App --> Models
    App --> DeploySvc
    App --> ConnectorSvc
    App --> JFrogSvc
    App --> ServiceNowSvc

    DeploySvc --> ApiSvc
    ConnectorSvc --> ApiSvc
    JFrogSvc --> ApiSvc
    ServiceNowSvc --> ApiSvc
    ApiSvc --> Env
    ApiSvc --> API
```

## Flujos MVP (referencia rapida)

- Registro de deploy:
  - Usuario -> Frontend -> `POST /api/deploys` -> BD
- Lookup de artifacto:
  - Usuario -> Frontend -> `POST /api/jfrog/builds/lookup` -> JFrog API
- Crear CHG:
  - Usuario -> Frontend -> `POST /api/servicenow/changes` -> ServiceNow API -> actualiza deploy con `CHG`
- Sync de estado CHG:
  - Usuario -> Frontend -> `POST /api/servicenow/sync/deploy/{id}` -> ServiceNow API -> actualiza `servicenow_status`
