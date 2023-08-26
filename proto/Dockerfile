# Start from a base image with Node.js
FROM node:20-slim

# Set up a working directory inside the container
WORKDIR /app

# Install necessary system packages and clean up after installation
RUN apt-get update && apt-get install -y protobuf-compiler python3 python3-pip && \
    pip3 install protobuf && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install the ts-protoc-gen npm package directly in the image
RUN npm install ts-protoc-gen && \
    chmod +x ./node_modules/ts-protoc-gen/bin/protoc-gen-ts

# Copy only necessary files and directories
COPY schemas ./schemas
COPY gen.sh ./gen.sh

# Set a non-root user and change ownership of the /app directory
RUN useradd -ms /bin/bash user && \
    chown -R user:user /app

USER user

# Set the entrypoint
ENTRYPOINT [ "sh", "./gen.sh" ]
