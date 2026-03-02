#!/bin/bash

# Install PM2 globally if not already installed
if ! command -v pm2 &> /dev/null; then
  echo "Installing PM2..."
  npm install -g pm2
fi

# Stop any existing PM2 process for todoastros
pm2 stop todoastros 2>/dev/null || true
pm2 delete todoastros 2>/dev/null || true

# Clean up the .next directory
rm -rf .next

# Build the application
echo "Building the application..."
npm run build

# Start the application with PM2
echo "Starting the application with PM2..."
pm2 start npm --name "todoastros" -- start

# Save the PM2 process list
pm2 save

# Set up PM2 to start on system boot
echo "Setting up PM2 to start on system boot..."
pm2 startup | tail -n 1

echo "✅ Application is now running with PM2"
echo "You can check the status with: pm2 status"
echo "You can view logs with: pm2 logs todoastros"

