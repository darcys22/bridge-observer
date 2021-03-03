APP_NAME=observer
FIND_PROCESS_ID=$(eval PROCESS_ID=$(shell docker ps -q --filter ancestor=$(APP_NAME)))

# DOCKER TASKS
# Build the container
build: ## Build the container
	docker build -t $(APP_NAME) .

build-nc: ## Build the container without caching
	docker build --no-cache -t $(APP_NAME) .

run: ## Run container as a daemon
	docker run -d $(APP_NAME)

stop: ## Kill the running container running as daemon
	$(FIND_PROCESS_ID)
	docker kill $(PROCESS_ID)
