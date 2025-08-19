# Empezamos con la imagen oficial de n8n
FROM docker.n8n.io/n8nio/n8n:latest

# --- TAREAS COMO USUARIO ROOT ---
USER root

# 1. Instalar dependencias del sistema
RUN apk add --update python3 py3-pip

# 2. Instalar librerías de Python globalmente
RUN python3 -m pip install --no-cache-dir --break-system-packages zep-cloud

# 3. Crear un nuevo directorio para nuestros helpers personalizados
RUN mkdir -p /app/helpers && chown -R node:node /app

# --- TAREAS COMO USUARIO NODE ---
USER node

# 4. Instalar herramientas de usuario como pipx
RUN python3 -m pip install --user --break-system-packages pipx

# 5. Copiar nuestro fichero de ayuda al nuevo directorio, no al que se solapa con el volumen
COPY --chown=node:node zep_helpers.py /app/helpers/zep_helpers.py

# 6. Añadir el nuevo directorio a la ruta de búsqueda de Python (PYTHONPATH)
ENV PYTHONPATH="/app/helpers:${PYTHONPATH}"

# 7. Añadir el directorio local de binarios de 'node' AL FINAL del PATH principal
ENV PATH="$PATH:/home/node/.local/bin"
