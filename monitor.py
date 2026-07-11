import json
import os
import smtplib
from datetime import datetime, timezone
from email.mime.text import MIMEText

import requests

SITES = [
    "https://phoneclinicpro.com/",
    "https://voosriopan.com/",
    "https://easyflighttour.com.br/",
    "https://intestinon.com.br/",
]

STATUS_FILE = os.path.join(os.path.dirname(__file__), "monitor-status.json")
TIMEOUT = 15

GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
ALERT_EMAIL_TO = os.environ["ALERT_EMAIL_TO"]


def checar_site(url):
    for _ in range(2):
        try:
            resposta = requests.get(url, timeout=TIMEOUT, allow_redirects=True)
            if resposta.status_code < 400:
                return True
        except requests.RequestException:
            pass
    return False


def enviar_email(assunto, corpo):
    msg = MIMEText(corpo)
    msg["Subject"] = assunto
    msg["From"] = GMAIL_USER
    msg["To"] = ALERT_EMAIL_TO
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
        servidor.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        servidor.send_message(msg)


def carregar_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    return {}


def salvar_status(status):
    with open(STATUS_FILE, "w", encoding="utf-8") as arquivo:
        json.dump(status, arquivo, ensure_ascii=False, indent=2)


def main():
    status_anterior = carregar_status()
    status_atual = {}
    agora = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")

    for url in SITES:
        online = checar_site(url)
        estava_online = status_anterior.get(url, {}).get("online", True)
        status_atual[url] = {"online": online, "verificado_em": agora}

        if estava_online and not online:
            enviar_email(
                f"Site fora do ar: {url}",
                f"O site {url} não respondeu corretamente na verificação das {agora}.\n\n"
                "Você vai receber um novo aviso quando ele voltar ao normal.",
            )
        elif not estava_online and online:
            enviar_email(
                f"Site voltou ao ar: {url}",
                f"O site {url} voltou a responder normalmente na verificação das {agora}.",
            )

    salvar_status(status_atual)


if __name__ == "__main__":
    main()
