FROM node:20-alpine AS build

LABEL org.opencontainers.image.title="EmploySight Frontend"
LABEL org.opencontainers.image.version="4.0.1"

WORKDIR /app

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

FROM nginx:1.27-alpine

LABEL org.opencontainers.image.title="EmploySight Frontend Runtime"
LABEL org.opencontainers.image.version="4.0.1"

COPY deploy/nginx/employsight.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
