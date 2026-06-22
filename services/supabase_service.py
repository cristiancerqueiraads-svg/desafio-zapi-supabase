import logging
from typing import Any

from supabase import Client, create_client
from supabase.lib.client_options import ClientOptions


def get_client(url: str, key: str) -> Client:
    """Cria e retorna um cliente autenticado do Supabase."""
    options = ClientOptions(postgrest_client_timeout=10)
    return create_client(url, key, options=options)


def fetch_contacts(client: Client, limit: int = 3) -> list[dict[str, Any]]:
    """Busca até *limit* contatos na tabela 'contatos'."""
    try:
        response = (
            client.table("contatos")
            .select("*")
            .limit(limit)
            .execute()
        )
        contacts: list[dict[str, Any]] = response.data
        logging.info(f"Contatos encontrados no Supabase: {len(contacts)}")
        return contacts
    except Exception:
        logging.exception("Falha ao consultar a tabela 'contatos' no Supabase.")
        raise
