#!/bin/bash

echo "Fixing Next.js application..."

# Clean up the .next directory completely
rm -rf .next

# Fix the package.json to ensure React versions are compatible
sed -i 's/"react": "^19.0.0"/"react": "^18.2.0"/g' package.json
sed -i 's/"react-dom": "^19.0.0"/"react-dom": "^18.2.0"/g' package.json

# Install dependencies with legacy peer deps
echo "Installing dependencies..."
npm install --legacy-peer-deps

# Build the application
echo "Building the application..."
npm run build

# Start the application in production mode
echo "Starting the application..."
PORT=3000 npm start > logs/nextjs.log 2>&1 &

echo "Waiting for Next.js to start..."
sleep 10

# Check if the application is running
if lsof -i:3000 | grep LISTEN > /dev/null; then
  echo "✅ Next.js started successfully on port 3000"
else
  echo "❌ Next.js failed to start. Checking logs..."
  tail -n 20 logs/nextjs.log
fi

