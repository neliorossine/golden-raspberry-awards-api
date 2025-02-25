# Usa uma imagem base leve do Python
FROM python:3.10-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Define variáveis de ambiente para otimização
ENV PYTHONIOENCODING=utf-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instala as ferramentas essenciais para dependências nativas
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Cria um usuário não root para rodar a aplicação
RUN useradd --create-home appuser
USER appuser

# Copia apenas o arquivo de dependências para otimizar o cache
COPY --chown=appuser:appuser requirements.txt requirements.txt

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte da aplicação
COPY --chown=appuser:appuser app/ /app

# Copia o diretório `data` contendo o CSV
COPY --chown=appuser:appuser data/ /app/data

# Exclui caches de compilação para reduzir o tamanho da imagem
RUN rm -rf ~/.cache/pip

# Expõe a porta padrão da aplicação
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "app.py"]
