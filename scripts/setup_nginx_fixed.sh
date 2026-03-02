#!/bin/bash

echo "Setting up Nginx configuration..."

# Copy the configuration file
sudo cp nginx_fixed.conf /etc/nginx/sites-available/todoastros

# Create a symbolic link
sudo ln -sf /etc/nginx/sites-available/todoastros /etc/nginx/sites-enabled/

# Remove default configuration if it exists
if [ -f /etc/nginx/sites-enabled/default ]; then
    sudo rm /etc/nginx/sites-enabled/default
fi

# Test the configuration
echo "Testing Nginx configuration..."
sudo nginx -t

# If the test is successful, restart Nginx
if [ $? -eq 0 ]; then
    echo "Restarting Nginx..."
    sudo systemctl restart nginx
    echo "✅ Nginx configuration has been updated"
else
    echo "❌ Nginx configuration test failed"
fi

