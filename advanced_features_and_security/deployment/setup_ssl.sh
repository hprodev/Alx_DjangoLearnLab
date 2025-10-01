#!/bin/bash

# SSL Certificate Setup Script for Let's Encrypt (Certbot)

# Update system packages
sudo apt update

# Install Certbot
sudo apt install certbot python3-certbot-nginx -y  # For Nginx
# sudo apt install certbot python3-certbot-apache -y  # For Apache

# Obtain SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com  # For Nginx
# sudo certbot --apache -d yourdomain.com -d www.yourdomain.com  # For Apache

# Set up automatic renewal
sudo crontab -e
# Add this line: 0 12 * * * /usr/bin/certbot renew --quiet

echo "SSL certificate setup completed!"
echo "Remember to update your DNS records to point to this server"
echo "Test your SSL configuration at: https://www.ssllabs.com/ssltest/"