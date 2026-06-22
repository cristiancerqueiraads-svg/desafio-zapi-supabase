#!/usr/bin/env bash
set -euo pipefail

echo "=== Setup do projeto Supabase + Z-API ==="

# Cria ambiente virtual
if [ ! -d ".venv" ]; then
    echo "[1/3] Criando ambiente virtual..."
    python3 -m venv .venv
else
    echo "[1/3] Ambiente virtual já existe."
fi

# Instala dependências
echo "[2/3] Instalando dependências..."
.venv/bin/pip install -r requirements.txt --quiet

# Cria .env se não existir
if [ ! -f ".env" ]; then
    echo "[3/3] Criando .env a partir do .env.example..."
    cp .env.example .env
    echo ""
    echo "⚠️  Edite o arquivo .env com suas credenciais antes de executar!"
    echo "   nano .env"
else
    echo "[3/3] .env já existe."
fi

echo ""
echo "✅ Setup concluído!"
echo ""
echo "Para executar:"
echo "   .venv/bin/python main.py"
