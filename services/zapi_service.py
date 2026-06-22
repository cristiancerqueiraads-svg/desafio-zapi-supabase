import logging

import requests


def _build_url(instance_id: str, instance_token: str, path: str) -> str:
    """Monta a URL base da API Z-API para um determinado endpoint."""
    return (
        f"https://api.z-api.io/instances/{instance_id}"
        f"/token/{instance_token}/{path}"
    )


def _build_headers(client_token: str | None) -> dict[str, str]:
    """Monta os cabeçalhos HTTP, incluindo Client-Token se fornecido."""
    headers = {"Content-Type": "application/json"}
    if client_token:
        headers["Client-Token"] = client_token
    return headers


def phone_exists(instance_id: str, instance_token: str, client_token: str | None, phone: str) -> bool | None:
    """Verifica se o número possui WhatsApp cadastrado.

    Retorna:
        True  → número existe no WhatsApp
        False → número não existe no WhatsApp
        None  → erro na consulta (timeout, conexão, etc.)
    """
    url = _build_url(instance_id, instance_token, f"phone-exists/{phone}")
    headers = _build_headers(client_token)

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            logging.warning(
                f"Z-API: phone-exists falhou para {phone} — "
                f"status {response.status_code} | {response.text}"
            )
            return None

        data = response.json()
        existe = data.get("exists", False)
        if existe:
            logging.info(f"Z-API: número {phone} existe no WhatsApp")
        else:
            logging.info(f"Z-API: número {phone} NÃO existe no WhatsApp")
        return existe

    except requests.exceptions.Timeout:
        logging.error(f"Z-API: timeout ao consultar phone-exists para {phone}")
        return None
    except requests.exceptions.ConnectionError:
        logging.error(f"Z-API: erro de conexão ao consultar phone-exists para {phone}")
        return None
    except requests.exceptions.RequestException:
        logging.exception(f"Z-API: erro inesperado ao consultar phone-exists para {phone}")
        return None


def send_text(instance_id: str, instance_token: str, client_token: str | None, phone: str, message: str) -> bool:
    """Envia uma mensagem de texto via Z-API e retorna True em caso de sucesso."""
    url = _build_url(instance_id, instance_token, "send-text")

    payload = {"phone": phone, "message": message}

    try:
        response = requests.post(url, json=payload, headers=_build_headers(client_token), timeout=15)

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


def get_send_status(instance_id: str, instance_token: str, client_token: str | None) -> list | None:
    """Retorna a fila de mensagens aguardando processamento.

    O endpoint espera um POST. Retorna uma lista de dicionários com o
    status de cada mensagem, ou None em caso de erro na consulta.
    """
    url = _build_url(instance_id, instance_token, "send-text-status")
    headers = _build_headers(client_token)
    payload = {"message": "consulta de status da fila"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)

        if response.status_code != 200:
            logging.warning(
                f"Z-API: send-text-status falhou — "
                f"status {response.status_code} | {response.text}"
            )
            return None

        data: list[dict] = response.json()
        logging.info(f"Z-API: fila de mensagens contém {len(data)} item(ns)")
        return data

    except requests.exceptions.Timeout:
        logging.error("Z-API: timeout ao consultar send-text-status")
        return None
    except requests.exceptions.ConnectionError:
        logging.error("Z-API: erro de conexão ao consultar send-text-status")
        return None
    except requests.exceptions.RequestException:
        logging.exception("Z-API: erro inesperado ao consultar send-text-status")
        return None
