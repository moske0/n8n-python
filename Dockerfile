
# 1. Imagen oficial de n8n (base Debian/Ubuntu)
FROM docker.n8n.io/n8nio/n8n:latest

# 2. Usuario root para instalar paquetes
USER root

# 3. Instalar Python 3, pip y venv en Debian/Ubuntu
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
       python3 python3-venv python3-pip ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 4. Crear entorno virtual en /opt/venv e instalar dependencias Python dentro
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && PIP_NO_CACHE_DIR=1 /opt/venv/bin/pip install zep-cloud serpapi \
    && chown -R node:node /opt/venv

# 5. Añadir el entorno virtual al PATH
ENV PATH="/opt/venv/bin:${PATH}"

# 6. Crear el directorio para scripts y cambiar permisos
RUN mkdir -p /app/scripts && chown -R node:node /app

# 7. Copiar los scripts
COPY --chown=node:node zep_utils.py /app/scripts/
COPY --chown=node:node crear_usuario_zep.py /app/scripts/
COPY --chown=node:node buscar_contexto.py /app/scripts/
COPY --chown=node:node grabar_recuerdos.py /app/scripts/
COPY --chown=node:node buscar_amazon.py /app/scripts/
COPY --chown=node:node buscar_local.py /app/scripts/
COPY --chown=node:node buscar_youtube.py /app/scripts/
COPY --chown=node:node buscar_google.py /app/scripts/

# (Opcional) Verificación en build de que los paquetes Python están disponibles
# RUN python -c "import zep_cloud, serpapi; print('Python OK')"

# 8. Volver al usuario no privilegiado
USER node
