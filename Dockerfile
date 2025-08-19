# Empezamos con la imagen oficial de n8n
FROM docker.n8n.io/n8nio/n8n:latest

# 2. Cambiamos a usuario root para instalar paquetes del sistema

USER root

# 3. Instala Python 3 y pip en Alpine (sin venv, no es necesario para tu caso)
RUN apk add --no-cache python3 py3-pip

# 4. Instala zep-cloud globalmente (no hace falta venv en Alpine para scripts de integración)

RUN pip3 install --upgrade pip && pip3 install zep-cloud

# 5. Crea el directorio /app/scripts donde vivirán nuestros scripts

RUN mkdir -p /app/scripts && chown -R node:node /app

# 6. Copia los nuevos scripts de Python a la imagen

COPY --chown=node:node zep_utils.py /app/scripts/
COPY --chown=node:node crear_usuario_zep.py /app/scripts/
COPY --chown=node:node buscar_contexto.py /app/scripts/
COPY --chown=node:node grabar_recuerdos.py /app/scripts/

# 7. Vuelve al usuario no privilegiado con el que corre n8n

USER node
