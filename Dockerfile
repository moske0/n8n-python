# Empezamos con la imagen oficial de n8n
FROM docker.n8n.io/n8nio/n8n:latest

# 2. Cambiamos a usuario root para instalar paquetes del sistema
USER root

# 3. Instala Python 3, pip y las herramientas para crear entornos virtuales
RUN apk add --no-cache python3 py3-pip python3-venv

# 4. Crea un entorno virtual en /opt/venv e instala zep-cloud dentro
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir zep-cloud

# 5. Crea el directorio /app/scripts donde vivirán nuestros scripts
RUN mkdir -p /app/scripts && chown -R node:node /app

# 6. Copia los nuevos scripts de Python a la imagen
COPY --chown=node:node zep_utils.py /app/scripts/
COPY --chown=node:node crear_usuario_zep.py /app/scripts/
COPY --chown=node:node buscar_contexto.py /app/scripts/
COPY --chown=node:node grabar_recuerdos.py /app/scripts/

# 7. Vuelve al usuario no privilegiado con el que corre n8n
USER node
