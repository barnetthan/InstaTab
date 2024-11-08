# Makefile
ARCH := $(shell uname -m)

FRONTEND_IMAGE=instatab-frontend:latest
BACKEND_IMAGE=instatab-backend:latest


# Define the default target
.PHONY: app clean

# Target to run Docker Compose
app:
	@echo "Starting the application using Docker Compose..."
	docker-compose up

# Build frontend based on architecture
# build-frontend:
# ifeq ($(ARCH), x86_64)
# 	@echo "Building frontend for amd64 architecture"
# 	docker buildx build --platform linux/amd64 -t $(FRONTEND_IMAGE) -f frontend/Dockerfile .
# else ifeq ($(ARCH), arm64)
# 	@echo "Building frontend for arm64 architecture"
# 	docker buildx build --platform linux/arm64 -t $(FRONTEND_IMAGE) -f frontend/Dockerfile .
# else
# 	@echo "Unsupported architecture: $(ARCH)"
# 	exit 1
# endif
build-frontend:
	docker build -t $(FRONTEND_IMAGE) -f frontend/Dockerfile .

build-backend:
	docker build -t $(BACKEND_IMAGE) -f backend/Dockerfile .

push-backend:
	docker tag instatab-backend aaronk2711/itbackend
	docker push aaronk2711/itbackend

push-frontend:
	docker tag instatab-frontend aaronk2711/itfrontend
	docker push aaronk2711/itfrontend

# # Build backend based on architecture
# build-backend:
# ifeq ($(ARCH), x86_64)
# 	@echo "Building backend for amd64 architecture"
# 	docker buildx build --platform linux/amd64 -t $(BACKEND_IMAGE) -f backend/Dockerfile .
# else ifeq ($(ARCH), arm64)
# 	@echo "Building backend for arm64 architecture"
# 	docker buildx build --platform linux/arm64 -t $(BACKEND_IMAGE) -f backend/Dockerfile .
# else
# 	@echo "Unsupported architecture: $(ARCH)"
# 	exit 1
# endif



# Target to stop and remove containers
clean:
	@echo "Stopping and removing containers..."
	docker-compose down

.PHONY: app build-frontend build-backend clean
