# Desafio Técnico — Integração Supabase + Z-API

Script em Python que lê contatos de uma tabela no **Supabase** e envia
mensagens personalizadas via **Z-API** (WhatsApp).

## Estrutura da tabela `contatos` (Supabase)

| Coluna     | Tipo     | Descrição                                |
|------------|----------|------------------------------------------|
| `id`       | `uuid`   | Chave primária (gerada automaticamente). |
| `nome`     | `text`   | Nome do contato.                         |
| `telefone` | `text`   | Número com DDI e DDD (`5511999999999`).  |

## Exemplo de `.env`

```env
SUPABASE_URL=sua_url_do_supabase_aqui
SUPABASE_KEY=sua_anon_key_do_supabase_aqui

ZAPI_INSTANCE=seu_instance_id_da_zapi
ZAPI_TOKEN=seu_instance_token_da_zapi
ZAPI_CLIENT_TOKEN=seu_client_token_da_zapi  # Opcional
```

## Instalação

```bash
pip install -r requirements.txt
```

## Execução

```bash
python main.py
```
