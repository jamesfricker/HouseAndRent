# !/bin/bash

# Desc: Generate proto files for python and javascript

# Usage: ./gen.sh

GEN_DIR="gen"
PYTHON_DIR="${GEN_DIR}/python"
JS_DIR="${GEN_DIR}/js"
SCHEMA_DIR="schemas"

mkdir -p ${PYTHON_DIR}
mkdir -p ${JS_DIR}
protoc -I="${SCHEMA_DIR}" --python_out="${PYTHON_DIR}" "${SCHEMA_DIR}/PredictRequest.proto"
protoc -I="${SCHEMA_DIR}" \
    --plugin=protoc-gen-ts=./node_modules/ts-protoc-gen/bin/protoc-gen-ts \
    --ts_out="${JS_DIR}" \
    "${SCHEMA_DIR}"/PredictRequest.proto
