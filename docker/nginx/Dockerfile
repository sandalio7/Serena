FROM nginx:1.21-alpine

# Eliminar la configuración predeterminada
RUN rm /etc/nginx/conf.d/default.conf

# Copiar nuestra configuración
COPY docker/nginx/default.conf /etc/nginx/conf.d/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]