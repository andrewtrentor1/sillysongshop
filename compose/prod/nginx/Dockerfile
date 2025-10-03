FROM nginx:1.27.3-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY ./compose/prod/nginx/nginx.conf /etc/nginx/conf.d
COPY ./assets /app/assets
