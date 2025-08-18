FROM docker.n8n.io/n8nio/n8n:latest

# Install python3
USER root
RUN apk add --update python3 py3-pip

# Add the path of the pipx installation to PATH
ENV PATH="/home/node/.local/bin:$PATH"

# Install Zep Cloud SDK for Python
RUN python3 -m pip install --no-cache-dir zep-cloud

USER node
RUN python3 -m pip install --user --break-system-packages pipx

# Copy the client initialization script
COPY zep_client.py /usr/src/app/zep_client.py
