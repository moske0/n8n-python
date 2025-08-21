# 1. Imagen oficial de n8n
FROM docker.n8n.io/n8nio/n8n:latest

# 2. Usuario root para instalar paquetes
USER root

# 3. Instala Python 3, pip y virtualenv en Alpine
RUN apk add --no-cache python3 py3-pip py3-virtualenv

# 4. Crea entorno virtual en /opt/venv e instala zep-cloud dentro
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install zep-cloud serpapi

# 5. Añade el entorno virtual al PATH
ENV PATH="/opt/venv/bin:${PATH}"

# 6. Crea el directorio para scripts y cambia permisos
RUN mkdir -p /app/scripts && chown -R node:node /app

# 7. Copia los scripts
COPY --chown=node:node zep_utils.py /app/scripts/
COPY --chown=node:node crear_usuario_zep.py /app/scripts/
COPY --chown=node:node buscar_contexto.py /app/scripts/
COPY --chown=node:node grabar_recuerdos.py /app/scripts/
COPY --chown=node:node buscar_amazon.py /app/scripts/
COPY --chown=node:node buscar_local.py /app/scripts/
COPY --chown=node:node buscar_youtube.py /app/scripts/
COPY --chown=node:node buscar_google.py /app/scripts/

# 8. Vuelve al usuario no privilegiado
USER node
