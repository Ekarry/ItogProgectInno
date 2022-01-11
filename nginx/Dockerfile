FROM nginx:latest
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY nginx.crt /etc/ssl/certs/nginx.crt
COPY nginx.key /etc/ssl/private/nginx.key
COPY nginx.pem /etc/ssl/certs/nginx.pem

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
