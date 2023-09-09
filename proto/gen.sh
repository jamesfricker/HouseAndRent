#!/bin/bash

# Desc: Generate proto files for python and javascript

# Usage: ./gen.sh

GEN_DIR="gen"
PYTHON_DIR="${GEN_DIR}/python/house_and_rent_api/"
TS_DIR="${GEN_DIR}/ts"
SCHEMA_DIR="schemas"

mkdir -p ${PYTHON_DIR}
mkdir -p ${TS_DIR}


# Navigate back to the original directory (where the script is being run)
cd -

find ${SCHEMA_DIR} -name "*.proto" | while read -r PROTO_FILE; do
    protoc -I="${SCHEMA_DIR}" --python_out="${PYTHON_DIR}" "${PROTO_FILE}"
    protoc -I="${SCHEMA_DIR}" \
        --plugin=protoc-gen-ts=./node_modules/ts-protoc-gen/bin/protoc-gen-ts \
        --ts_out="${TS_DIR}" \
        "${PROTO_FILE}"
done

# Create __init__.py in the newly generated directories within the PYTHON_DIR
# This is to ensure that each directory that's created for the proto packages has an __init__.py
find ${PYTHON_DIR} -type d | while read -r DIR; do
    touch "${DIR}/__init__.py"
done

echo "Generation completed."
