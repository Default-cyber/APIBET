FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Como já usamos a imagem oficial do Playwright, precisamos apenas instalar os browsers do Python
RUN playwright install chromium

COPY . .

# Iniciar o Uvicorn. O Render injeta a porta na variável de ambiente PORT.
# Como o CMD padrão executa em shell, $PORT será substituído.
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
