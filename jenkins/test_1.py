import requests
from urllib.parse import urljoin

# === CONFIGURACIÓN BÁSICA ===
BASE_URL = "https://<tu-dominio>/cbci-controller-cbt/"  # termina en /
USER = "<tu_usuario_jenkins>"
API_TOKEN = "<tu_token>"  # token que ya generaste

# Si tu instalación usa Basic Auth clásico (lo más común)
session = requests.Session()
session.auth = (USER, API_TOKEN)

# Si usas token tipo Bearer (descomenta esto y comenta la línea de arriba):
# session = requests.Session()
# session.headers.update({"Authorization": f"Bearer {API_TOKEN}"})


def get_json(url, params=None):
    """Wrapper simple para peticiones GET + manejo básico de errores."""
    resp = session.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def collect_pipelines(base_url: str):
    """
    Recorre recursivamente el árbol de jobs y devuelve una lista de
    pipelines (WorkflowJob y WorkflowMultiBranchProject).
    """
    pipelines = []

    def visit(api_url: str):
        # api_url típicamente: https://.../cbci-controller-cbt/api/json
        data = get_json(api_url, params={
            "tree": "jobs[name,fullName,url,_class]"
        })

        for job in data.get("jobs", []):
            jclass = job.get("_class", "")
            jurl = job.get("url")

            # Pipelines simples
            if jclass == "org.jenkinsci.plugins.workflow.job.WorkflowJob":
                pipelines.append(job)

            # Multibranch Pipelines
            elif jclass == "org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject":
                pipelines.append(job)

            # Carpetas (CloudBees Folders, etc.)
            elif jclass == "com.cloudbees.hudson.plugins.folder.Folder":
                # Navegamos dentro de la carpeta
                folder_api_url = urljoin(jurl, "api/json")
                visit(folder_api_url)

            # Otros tipos de job, los ignoramos

    root_api = urljoin(base_url, "api/json")
    visit(root_api)
    return pipelines


if __name__ == "__main__":
    pipelines = collect_pipelines(BASE_URL)

    print(f"Se encontraron {len(pipelines)} pipelines:\n")
    for p in pipelines:
        name = p.get("name")
        full_name = p.get("fullName")
        url = p.get("url")
        jclass = p.get("_class")
        print(f"- {full_name} ({jclass})")
        print(f"  URL: {url}")
