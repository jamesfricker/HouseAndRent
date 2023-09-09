# Start from a base image with Node.js
FROM node:20-slim

# Set up a working directory inside the container
WORKDIR /app

# Install necessary system packages. Use a single RUN command to reduce image layers.
RUN apt-get update && apt-get install -y \
    protobuf-compiler \
    python3 \
    python3-pip \
    python3-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    # Create a virtual environment
    && python3 -m venv /app/venv


# Activate the virtual environment for subsequent commands
ENV PATH="/app/venv/bin:$PATH"

# Install Python protobuf within the virtual environment
RUN pip install protobuf

# Install the ts-protoc-gen npm package directly in the image
RUN npm install ts-protoc-gen \
    && chmod +x ./node_modules/ts-protoc-gen/bin/protoc-gen-ts

# Copy only necessary files and directories
COPY schemas ./schemas
COPY gen.sh ./gen.sh

# Set a non-root user and change ownership of the /app directory
RUN useradd -ms /bin/bash user && \
    chown -R user:user /app

USER user

# Set the entrypoint
ENTRYPOINT [ "sh", "./gen.sh" ]
