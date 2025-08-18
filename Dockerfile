# Empezamos con la imagen oficial de n8n
FROM docker.n8n.io/n8nio/n8n:latest

# --- TAREAS COMO USUARIO ROOT ---
# Cambiamos a root para poder instalar paquetes del sistema
USER root

# 1. Instalar python y pip usando el gestor de paquetes de Alpine
RUN apk add --update python3 py3-pip

# 2. Instalar el SDK de Zep para que esté disponible para todos los usuarios
#    Añadimos la bandera --break-system-packages para confirmar la instalación
RUN python3 -m pip install --no-cache-dir --break-system-packages zep-cloud

# --- TAREAS COMO USUARIO NODE ---
# Volvemos al usuario 'node', que es con el que se ejecuta n8n
USER node

# 3. Instalar pipx como una herramienta solo para el usuario 'node'
RUN python3 -m pip install --user --break-system-packages pipx

# 4. Copiar tu script de cliente (opcional, ver nota abajo)
COPY zep_client.py /home/node/zep_client.py

# 5. Añadir el directorio local de binarios de 'node' AL FINAL del PATH
#    Esto es más seguro que ponerlo al principio
ENV PATH="$PATH:/home/node/.local/bin"
