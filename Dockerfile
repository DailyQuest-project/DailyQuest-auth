# --- Estágio 1: O "Builder" ---
# Instala dependências e compila pacotes (se necessário)
FROM python:3.10-slim AS builder

ENV DEBIAN_FRONTEND=noninteractive

# 1. Instala libs de sistema (só o essencial)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    libyaml-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 2. Instala dependências Python em um local separado
RUN pip install --upgrade pip setuptools wheel
WORKDIR /app
COPY requirements.txt .
RUN pip install --prefix="/install" -r requirements.txt


# --- Estágio 2: O "Final" ---
# Imagem limpa que só roda a aplicação
FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive

# 1. Instala a dependência de *runtime* do PyYAML
RUN apt-get update && apt-get install -y --no-install-recommends \
    libyaml-0-2 \
    && rm -rf /var/lib/apt/lists/*

# 2. Copia as dependências pré-instaladas do "builder"
COPY --from=builder /install /usr/local

# 3. Copia o código da aplicação
WORKDIR /app
COPY . .

EXPOSE 8080

# 4. Comando para executar a aplicação
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]