# Use the Nginx image
FROM nginx

EXPOSE 80
EXPOSE 443

# Remove the default nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

# Replace with our own nginx.conf
COPY nginx.conf /etc/nginx/conf.d/

COPY public.crt /etc/ssl/certs/
COPY private.key /etc/ssl/private/
