# Desafio Técnico — Integração Supabase + Z-API

Script em Python que lê contatos de uma tabela no **Supabase** e envia
mensagens personalizadas via **Z-API** (WhatsApp).

## 🧱 Pré-requisitos

- Python 3.10+
- Conta no [Supabase](https://supabase.com) com uma tabela `contatos`
- Conta na [Z-API](https://www.z-api.io) com uma instância configurada

## 📦 Versões utilizadas (validadas)

| Pacote       | Versão  | Observação                                      |
|--------------|---------|-------------------------------------------------|
| Python       | 3.12    | Qualquer versão 3.10+ funciona                  |
| `supabase`   | 2.3.4   |                                                 |
| `requests`   | 2.31.0  |                                                 |
| `python-dotenv` | 1.0.1 |                                                 |
| `httpx`      | < 0.24  | ⚠️ Versões >= 0.24 quebram com a `gotrue` atual |

> ⚠️ **Importante:** a `gotrue` (dependência interna do `supabase`) não é compatível com `httpx>=0.24`. Por isso o `requirements.txt` já trava o `httpx` na versão correta.

## 🗄️ Estrutura da tabela `contatos` (Supabase)

| Coluna     | Tipo     | Descrição                                |
|------------|----------|------------------------------------------|
| `id`       | `uuid`   | Chave primária (gerada automaticamente). |
| `nome`     | `text`   | Nome do contato.                         |
| `telefone` | `text`   | Número com DDI e DDD (`5511999999999`).  |

### Script SQL para criar a tabela direto no Supabase

```sql
CREATE TABLE contatos (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    nome text NOT NULL,
    telefone text NOT NULL
);
```

## ⚙️ Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
```

### 2. Crie o arquivo `.env`

Copie o arquivo de exemplo e preencha com suas credenciais:

```bash
cp .env.example .env
```

Edite o `.env` com seus dados:

```env
# Supabase
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_anon_key_do_supabase

# Z-API
ZAPI_INSTANCE=seu_instance_id_da_zapi
ZAPI_TOKEN=seu_instance_token_da_zapi
ZAPI_CLIENT_TOKEN=seu_client_token_da_zapi  # Opcional
```

**Onde conseguir cada credencial:**

| Variável            | Onde encontrar                                                                 |
|---------------------|--------------------------------------------------------------------------------|
| `SUPABASE_URL`      | Settings → API → Project URL (sem `/rest/v1/`)                                |
| `SUPABASE_KEY`      | Settings → API → `anon` public key                                            |
| `ZAPI_INSTANCE`     | Z-API → Instância → `id` (só o UUID, não a URL completa)                      |
| `ZAPI_TOKEN`        | Z-API → Instância → `token`                                                   |
| `ZAPI_CLIENT_TOKEN` | Z-API → Instância → `Client-Token` (só se o segurança estiver ativada)        |

### 3. Crie o ambiente virtual e instale as dependências

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Execute o script

```bash
python main.py
```

### 5. Exemplo de saída esperada

```
2026-06-22 11:43:39 - INFO - === Início da execução ===
2026-06-22 11:43:40 - INFO - Contatos encontrados no Supabase: 1
2026-06-22 11:43:40 - INFO - Processando 1 contato(s)...
2026-06-22 11:43:40 - INFO - Enviando mensagem para <nome de usuario> (5511922223333)...
2026-06-22 11:43:40 - INFO - Z-API: mensagem enviada com sucesso para 5511922223333 (status 200)
2026-06-22 11:43:40 - INFO - Mensagem enviada com sucesso para <nome de usuario> (5511922223333).
2026-06-22 11:43:40 - INFO - === Fim da execução ===
```

## 🐛 Troubleshooting

### `Client.__init__() got an unexpected keyword argument 'proxy'`

Ocorre quando a versão do `httpx` é incompatível com a `gotrue` (dependência do Supabase).

**Solução:** instale uma versão compatível do httpx:

```bash
pip install "httpx<0.24"
```

## 🚀 Script de setup rápido (Linux / macOS)

```bash
chmod +x setup.sh
./setup.sh
```
