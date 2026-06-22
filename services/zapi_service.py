import logging

import requests


def send_text(instance_id: str, instance_token: str, client_token: str | None, phone: str, message: str) -> bool:
    """Envia uma mensagem de texto via Z-API e retorna True em caso de sucesso."""
    url = (
        f"https://api.z-api.io/instances/{instance_id}"
        f"/token/{instance_token}/send-text"
    )

    headers = {"Content-Type": "application/json"}
    if client_token:
        headers["Client-Token"] = client_token

    payload = {"phone": phone, "message": message}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)

        if response.status_code in (200, 201):
            logging.info(f"Z-API: mensagem enviada com sucesso para {phone} (status {response.status_code})")
            return True

        logging.warning(
            f"Z-API: falha ao enviar para {phone} — status {response.status_code} | resposta: {response.text}"
        )
        return False

    except requests.exceptions.Timeout:
        logging.error(f"Z-API: timeout ao enviar mensagem para {phone}")
        return False
    except requests.exceptions.ConnectionError:
        logging.error(f"Z-API: erro de conexão ao enviar mensagem para {phone}")
        return False
    except requests.exceptions.RequestException:
        logging.exception(f"Z-API: erro inesperado ao enviar mensagem para {phone}")
        return False
