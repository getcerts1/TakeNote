FROM nginx
COPY /nginx/default.conf /etc/nginx/conf.d/default.conf
COPY frontend /usr/share/nginx/html

EXPOSE 80

#remember, if you set your context to the project folder, docker resolves file paths relative
# to the project directory. This means building images must specify files relative to the project folder
