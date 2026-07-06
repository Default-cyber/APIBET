#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Instalando dependencias do Python..."
pip install -r requirements.txt

echo "Instalando Playwright..."
playwright install chromium

echo "Instalando dependencias de sistema do Playwright (isso pode demorar no free tier)..."
# Render suporta install-deps no Ubuntu
playwright install-deps chromium

echo "Build concluido com sucesso!"
