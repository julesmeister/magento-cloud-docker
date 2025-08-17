FROM php:8.2-fpm

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libfreetype6-dev \
    libjpeg62-turbo-dev \
    libpng-dev \
    libzip-dev \
    libxml2-dev \
    libxslt1-dev \
    libicu-dev \
    git \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install PHP extensions required by Magento
RUN docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j$(nproc) \
        bcmath \
        gd \
        intl \
        pdo_mysql \
        soap \
        xsl \
        zip \
        sockets \
        opcache

# Install Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Set working directory
WORKDIR /var/www/html

# Set proper permissions
RUN chown -R www-data:www-data /var/www/html