# Multi-stage Dockerfile for React Travel Chat UI
# Optimized for Azure Container Apps on Linux with HTTPS (port 443)

# Stage 1: Build the React application
FROM node:18-alpine AS builder

# Build arguments for environment variables
ARG REACT_APP_AUTH_USERNAME
ARG REACT_APP_AUTH_PASSWORD
ARG REACT_APP_API_URL

# Set environment variables for the build process
ENV REACT_APP_AUTH_USERNAME=${REACT_APP_AUTH_USERNAME}
ENV REACT_APP_AUTH_PASSWORD=${REACT_APP_AUTH_PASSWORD}
ENV REACT_APP_API_URL=${REACT_APP_API_URL}

# Set working directory
WORKDIR /app

# Copy package.json for dependency installation
COPY package.json ./

# Set npm configuration for better compatibility
RUN npm config set fetch-retry-mintimeout 20000 && \
    npm config set fetch-retry-maxtimeout 120000 && \
    npm config set fetch-retries 3 && \
    npm cache clean --force

# Install dependencies with legacy peer deps to avoid conflicts
RUN npm install --legacy-peer-deps --silent --no-fund --no-audit

# Copy source code
COPY . .

# Set build environment variables
ENV GENERATE_SOURCEMAP=false
ENV CI=true
ENV NODE_OPTIONS=--max_old_space_size=4096

# Build the React application for production
# Environment variables are embedded during build
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
