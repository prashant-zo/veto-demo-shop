.PHONY: build

SHA := $(shell git rev-parse --short HEAD)
TAG := $(if $(PR),pr-$(PR)-$(SHA),main-$(SHA))
IMAGE := veto-shop:$(TAG)

build: ## build the image and load it into kind
	docker build -t $(IMAGE) .
	kind load docker-image $(IMAGE) --name veto
	@echo "loaded $(IMAGE)"
