FROM nginx:latest
COPY --from=builder ./nginx.conf /etc/nginx/conf.d/default.conf
COPY ./nginx.crt /etc/ssl/certs/nginx.crt
COPY ./nginx.key /etc/ssl/private/nginx.key

EXPOSE 80 443
CMD ["nginx", "-g", "daemon off;"]
