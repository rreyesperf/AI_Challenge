# Multi-stage Dockerfile for React Travel Chat UI
# Optimized for Azure Container Apps on Linux with HTTPS (port 443)

# Stage 1: Build the React application
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json for dependency installation
COPY package*.json ./

# Install dependencies
# Use npm ci for faster, reliable, reproducible builds in production
RUN npm ci --only=production --silent

# Copy source code
COPY . .

# Build the React application for production
# This creates an optimized production build in the /build directory
RUN npm run build

# Stage 2: Serve the built application with Nginx
FROM nginx:1.25-alpine AS production

# Install curl for health checks (required for Azure Container Apps)
RUN apk add --no-cache curl

# Remove default Nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Create custom Nginx configuration for React SPA
# This configuration handles React Router and serves static files efficiently
COPY <<EOF /etc/nginx/conf.d/default.conf
server {
    listen 8080;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    # Security headers for production
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Gzip compression for better performance
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

    # Cache static assets for better performance
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        try_files \$uri =404;
    }

    # Handle React Router routes (SPA fallback)
    # All routes should serve index.html to let React Router handle routing
    location / {
        try_files \$uri \$uri/ /index.html;
        
        # Prevent caching of index.html to ensure updates are reflected
        add_header Cache-Control "no-cache, no-store, must-revalidate";
        add_header Pragma "no-cache";
        add_header Expires "0";
    }

    # API proxy configuration (optional - if backend is on same domain)
    # Uncomment and modify if you need to proxy API calls
    # location /api/ {
    #     proxy_pass http://backend-service:5000;
    #     proxy_set_header Host \$host;
    #     proxy_set_header X-Real-IP \$remote_addr;
    #     proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    #     proxy_set_header X-Forwarded-Proto \$scheme;
    # }

    # Health check endpoint for Azure Container Apps
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
EOF

# Copy built React application from builder stage
COPY --from=builder /app/build /usr/share/nginx/html

# Create non-root user for security (Azure Container Apps best practice)
RUN addgroup -g 1000 -S nginx && \
    adduser -u 1000 -D -S -G nginx nginx

# Change ownership of Nginx directories to non-root user
RUN chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /etc/nginx/conf.d && \
    chown -R nginx:nginx /usr/share/nginx/html

# Create nginx.pid directory with proper permissions
RUN mkdir -p /var/run && \
    chown -R nginx:nginx /var/run

# Switch to non-root user
USER nginx

# Expose port 8080 (Azure Container Apps will map this to 443 externally)
EXPOSE 8080

# Add health check for container monitoring
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Start Nginx in foreground mode (required for containers)
CMD ["nginx", "-g", "daemon off;"]

# Build arguments for environment variables (can be overridden at build time)
ARG REACT_APP_API_URL
ENV REACT_APP_API_URL=${REACT_APP_API_URL}

# Metadata labels for Azure Container Apps
LABEL maintainer="Travel Chat Assistant Team"
LABEL description="React UI for Travel Chat Assistant - Azure Container Apps"
LABEL version="1.0.0"
LABEL org.opencontainers.image.source="https://github.com/yourusername/travel-chat-assistant"
