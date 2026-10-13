# NEBULA Frontend Multi-Stage Dockerfile

# Stage 1: Build production bundle
FROM node:22-alpine AS build

WORKDIR /app

# Copy package descriptors and install dependencies
COPY package*.json ./
RUN npm install

# Copy frontend source files
COPY . .

# Build production distribution bundle
RUN npm run build

# Stage 2: Serve via Nginx
FROM nginx:alpine

# Copy built distribution from build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy Nginx SPA reverse proxy configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose HTTP port
EXPOSE 80 5173

CMD ["nginx", "-g", "daemon off;"]
