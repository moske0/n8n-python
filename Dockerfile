# Empezamos con la imagen oficial de n8n
FROM docker.n8n.io/n8nio/n8n:latest

# --- TAREAS COMO USUARIO ROOT ---
# Cambiamos a root para poder instalar paquetes del sistema
USER root

# 1. Instalar python y pip usando el gestor de paquetes de Alpine
RUN apk add --update python3 py3-pip

# 2. Instalar el SDK de Zep para que esté disponible para todos los usuarios
RUN python3 -m pip install --no-cache-dir --break-system-packages zep-cloud


# --- TAREAS COMO USUARIO NODE ---
# Volvemos al usuario 'node', que es con el que se ejecuta n8n
USER node

# 3. Instalar pipx como una herramienta solo para el usuario 'node'
RUN python3 -m pip install --user --break-system-packages pipx

# 4. Copiar el fichero de ayuda al directorio de n8n
#    n8n añade automáticamente /home/node/.n8n a la ruta de Python, 
#    por lo que podremos importarlo directamente.
COPY --chown=node:node zep_helpers.py /home/node/.n8n/zep_helpers.py

# 5. Añadir el directorio local de binarios de 'node' AL FINAL del PATH
ENV PATH="$PATH:/home/node/.local/bin"
