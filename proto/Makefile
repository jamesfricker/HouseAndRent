
SHELL := /bin/bash


docker-gen:
	docker build -t proto-generator .
	docker run -v $$(pwd)/gen:/app/gen proto-generator

proto-clean:
	rm -rf proto/gen/*
