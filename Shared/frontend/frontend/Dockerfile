FROM php:7.2-apache
#EXPOSE 80
COPY . /app
WORKDIR /app
RUN docker-php-source extract \
    install -r requirements.txt \
    && docker-php-source delete
ENV FLASK_APP=app.py
CMD ["./wait-for-it.sh", "messaging:5672", "--", \
     "flask", "run", "--host=0.0.0.0"]

