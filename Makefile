# Makefile

# Define the default target
.PHONY: app clean

# Target to run Docker Compose
app:
	@echo "Starting the application using Docker Compose..."
	docker-compose up --build

# Target to stop and remove containers
clean:
	@echo "Stopping and removing containers..."
	docker-compose down
