FROM prestashop/prestashop:1.7.8

RUN apt-get update && apt-get install -y libmemcached-dev && \
    pecl install -f memcached && \
    docker-php-ext-enable memcached && \
    apt-get clean

RUN rm -rf /var/www/html/*

COPY src /var/www/html
COPY data/cert.pem /etc/ssl/certs/
COPY data/key.pem /etc/ssl/private/
COPY data/presta.conf /etc/apache2/sites-available/
COPY data/db.sql /db_dump/

RUN update-ca-certificates && \
    a2enmod ssl && \
    a2ensite presta && \
    chmod -R 755 /etc/apache2/sites-available /etc/ssl/certs /etc/ssl/private /db_dump

RUN chmod -R 755 /var/www/html && \
    chown -R www-data:www-data /var/www/html

CMD ["apache2-foreground"]
