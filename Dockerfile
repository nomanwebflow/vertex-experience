# Use official Nginx image
FROM nginx:alpine

# Copy application files to Nginx default directory
COPY . /usr/share/nginx/html

# Cloud Run expects the container to listen on $PORT
# Nginx listens on 80 by default. We can use a template or just sed the config on startup.
# We'll replace the listen port in the default config.

CMD sed -i -e 's/80/'"$PORT"'/g' /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'
