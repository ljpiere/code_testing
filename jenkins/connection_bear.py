import requests

BASE_URL = "https://<tu-dominio>/cbci-controller-cbt/"
API_TOKEN = "<tu_access_token_cloudbees>"  # el que generaste en la UI de CloudBees

session = requests.Session()
session.verify = False  # por tu problema de certificado
session.headers.update({
    "Authorization": f"Bearer {API_TOKEN}"
})

r = session.get(BASE_URL + "me/api/json", timeout=30)
print(r.status_code, r.text[:200])
