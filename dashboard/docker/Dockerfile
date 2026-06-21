FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl

# Instalar Poetry
ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Evita pasta __pycache__ (não beneficia containers)
ENV PYTHONDONTWRITEBYTECODE=1

# Configurar diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY pyproject.toml poetry.lock* ./

# Instalar dependências via Poetry (sem criar ambiente virtual dentro do container)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . ./

EXPOSE 8501

CMD ["poetry", "run", "streamlit", "run", "app.py"]