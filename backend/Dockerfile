# Use Python as the base image for the backend
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy requirements.txt
COPY backend/requirements.txt ./

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt
# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the backend code
COPY backend ./

# Expose the backend port (e.g., 5000 for Flask)
EXPOSE 5000

# Set environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
# Change to "production" for production

# Command to run the app
CMD ["flask", "run", "--host=0.0.0.0"]
