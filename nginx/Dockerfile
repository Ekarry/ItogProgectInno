FROM nginx:latest
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY nginx.crt /etc/ssl/certs/nginx.crt
COPY nginx.key /etc/ssl/private/nginx.key

EXPOSE 80 
CMD ["nginx", "-g", "daemon off;"]
