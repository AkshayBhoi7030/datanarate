# Use official Node.js image as base
FROM node:20-slim

# Set working directory
WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy frontend code
COPY frontend/ .

# Command to run the application
CMD ["npm", "run", "dev"]
