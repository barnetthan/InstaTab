# Use Node.js as the base image for the frontend
FROM node:16 AS frontend

# Set the working directory
WORKDIR /app

# Copy only package.json first to leverage Docker caching
COPY frontend/package.json ./

# Install dependencies and generate package-lock.json
RUN npm install

# Copy the rest of the frontend code
COPY frontend ./

# Build the frontend
RUN npm run build

# Use a lightweight web server to serve the built files
FROM nginx:alpine

# Copy built files to nginx
COPY --from=frontend /app/dist /usr/share/nginx/html

# Expose port 3000
EXPOSE 3000

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
