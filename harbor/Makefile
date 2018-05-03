
DOCKER_IMAGE_NAME	?= hub.meiqia.com/devops/harbor
DOCKER_IMAGE_TAG	?= $(shell cat VERSION) 

.PHONY: all
docker:
	@echo ">> building docker image"
	@docker build -t $(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG) .

install:
	@pip install -r requirement.txt -i https://pypi.douban.com/simple
