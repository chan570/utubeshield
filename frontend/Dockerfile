# Production Dockerfile for TubeShield AI React Frontend
FROM node:20-alpine as build-stage

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Stage 2: Serve static app using Nginx
FROM nginx:alpine

COPY --from=build-stage /app/dist /usr/share/nginx/html

# Custom Nginx SPA Routing config
RUN echo 'server { listen 80; location / { root /usr/share/nginx/html; index index.html; try_files $uri $uri/ /index.html; } }' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
