import logging
import os

from dotenv import load_dotenv

from services.supabase_service import fetch_contacts, get_client
from services.zapi_service import send_text
from utils.logger import setup_logger


def _load_env_or_raise(key: str) -> str:
    """Retorna o valor da variável de ambiente ou levanta um erro."""
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Variável de ambiente '{key}' não foi definida no arquivo .env")
    return value


def main() -> None:       #colocar todas as credenciais
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

    logger.info(f"Processando {len(contatos)} contato(s)...") #envio da mensagem, parei aqui!!!!

    for contato in contatos:
        nome = contato.get("nome", "").strip()
        telefone = contato.get("telefone", "").strip()

        if not nome or not telefone:
            logger.warning(f"Contato ignorado — campos 'nome' ou 'telefone' ausentes: {contato}")
            continue

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
        else:
            logger.error(f"Falha no envio da mensagem para {nome} ({telefone}).")

    logger.info("=== Fim da execução ===")


if __name__ == "__main__":
    main()
