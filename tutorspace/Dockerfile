
FROM node:12.2.0-alpine
WORKDIR /app

COPY ./* /app/
RUN npm install
RUN npm run build

FROM nginx
COPY --from=0 ./build/* /usr/share/nginx/html/
expose 80


