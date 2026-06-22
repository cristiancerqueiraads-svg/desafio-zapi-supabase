import logging
import os

from dotenv import load_dotenv

from services.supabase_service import fetch_contacts, get_client
from services.zapi_service import get_send_status, phone_exists, send_text
from utils.logger import setup_logger


def _load_env_or_raise(key: str) -> str:
    """Retorna o valor da variável de ambiente ou levanta um erro."""
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Variável de ambiente '{key}' não foi definida no arquivo .env")
    return value


def main() -> None:
    setup_logger()
    load_dotenv()

    logger = logging.getLogger(__name__)
    logger.info("=== Início da execução ===")

    try:
        supabase_url = _load_env_or_raise("SUPABASE_URL")
        supabase_key = _load_env_or_raise("SUPABASE_KEY")
        zapi_instance = _load_env_or_raise("ZAPI_INSTANCE")
        zapi_token = _load_env_or_raise("ZAPI_TOKEN")
    except ValueError as e:
        logger.error(e)
        return

    zapi_client_token = os.getenv("ZAPI_CLIENT_TOKEN")

    try:
        supabase = get_client(supabase_url, supabase_key)
        contatos = fetch_contacts(supabase, limit=3)
    except Exception:
        logger.error("Execução interrompida devido a erro na consulta ao Supabase.")
        return

    if not contatos:
        logger.warning("Nenhum contato encontrado. Nada a fazer.")
        return

    logger.info(f"Processando {len(contatos)} contato(s)...")

    enviados = 0
    pulados = 0

    for contato in contatos:
        nome = contato.get("nome", "").strip()
        telefone = contato.get("telefone", "").strip()

        if not nome or not telefone:
            logger.warning(f"Contato ignorado — campos 'nome' ou 'telefone' ausentes: {contato}")
            continue

        # 1. Verifica se o número existe no WhatsApp
        logger.info(f"Verificando número {telefone} ({nome})...")
        existe = phone_exists(zapi_instance, zapi_token, zapi_client_token, telefone)

        if existe is None:
            logger.warning(f"Pulando {nome} ({telefone}) — não foi possível verificar o número.")
            pulados += 1
            continue

        if not existe:
            logger.warning(f"Pulando {nome} ({telefone}) — número não possui WhatsApp.")
            pulados += 1
            continue

        # 2. Envia a mensagem
        mensagem = f"Olá, {nome} tudo bem com você?"
        logger.info(f"Enviando mensagem para {nome} ({telefone})...")

        sucesso = send_text(
            instance_id=zapi_instance,
            instance_token=zapi_token,
            client_token=zapi_client_token,
            phone=telefone,
            message=mensagem,
        )

        if sucesso:
            logger.info(f"Mensagem enviada com sucesso para {nome} ({telefone}).")
            enviados += 1
        else:
            logger.error(f"Falha no envio da mensagem para {nome} ({telefone}).")

    logger.info(f"Resumo: {enviados} enviado(s), {pulados} pulado(s), {len(contatos)} total.")

    # 3. Exibe status da fila
    logger.info("Consultando fila de mensagens...")
    fila = get_send_status(zapi_instance, zapi_token, zapi_client_token)
    if fila is not None:
        for item in fila:
            if isinstance(item, dict):
                phone = item.get("phone", "?")
                status = item.get("status", "?")
                logger.info(f"  Fila — telefone: {phone} | status: {status}")
            else:
                logger.info(f"  Fila — {item}")

    logger.info("=== Fim da execução ===")


if __name__ == "__main__":
    main()
