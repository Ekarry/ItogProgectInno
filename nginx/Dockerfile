FROM nginx:latest
COPY nginx.conf /etc/nginx/conf.d/default.conf
#COPY site.crt /etc/ssl/certs/site.crt
#COPY site.key /etc/ssl/private/site.key

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
