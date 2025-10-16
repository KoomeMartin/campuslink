# Frontend Dockerfile for CMU-Africa Campus Assistant
# Multi-stage build: Node.js for building, nginx for serving

# Build stage
FROM node:20-bullseye AS builder

# Set working directory
WORKDIR /app

ENV NEXT_TELEMETRY_DISABLED=1

# Install build tools
RUN apt-get update && apt-get install -y python3 make g++ bash


# Copy dependency manifests and install deps
COPY package.json ./
# RUN npm install --legacy-peer-deps
# RUN npm ci --production=false --omit=dev --no-audit --no-fund

RUN npm install --legacy-peer-deps

# Copy application files
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built files from build stage
COPY --from=build /app/build /usr/share/nginx/html

# Create nginx cache directory
RUN mkdir -p /var/cache/nginx/client_temp && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
