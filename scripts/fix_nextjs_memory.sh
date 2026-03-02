#!/bin/bash

echo "Fixing Next.js application with memory optimization..."

# Kill any existing Node.js processes
echo "Stopping any running Node.js processes..."
pkill -f node || true

# Clean up the .next directory completely
rm -rf .next

# Create a directory for logs if it doesn't exist
mkdir -p logs

# Fix the package.json to ensure React versions are compatible
sed -i 's/"react": "^19.0.0"/"react": "^18.2.0"/g' package.json
sed -i 's/"react-dom": "^19.0.0"/"react-dom": "^18.2.0"/g' package.json

# Install dependencies with reduced memory usage
echo "Installing dependencies with reduced memory usage..."
NODE_OPTIONS="--max-old-space-size=512" npm install --legacy-peer-deps

# Build the application with increased memory limit but in development mode first
echo "Building the application in development mode first..."
NODE_OPTIONS="--max-old-space-size=1024" npm run dev > logs/nextjs-dev.log 2>&1 &

# Wait for dev server to start
echo "Waiting for dev server to start (30 seconds)..."
sleep 30

# Kill the dev server
echo "Stopping dev server..."
pkill -f "node.*next dev" || true

# Now try to build for production with increased memory limit
echo "Now building for production..."
NODE_OPTIONS="--max-old-space-size=1024" npm run build

# Check if build was successful
if [ $? -eq 0 ]; then
  echo "✅ Build completed successfully!"
  
  # Start the application in production mode
  echo "Starting the application..."
  PORT=3000 NODE_OPTIONS="--max-old-space-size=512" npm start > logs/nextjs.log 2>&1 &
  
  echo "Waiting for Next.js to start..."
  sleep 10
  
  # Check if the application is running
  if lsof -i:3000 | grep LISTEN > /dev/null; then
    echo "✅ Next.js started successfully on port 3000"
  else
    echo "❌ Next.js failed to start. Checking logs..."
    tail -n 20 logs/nextjs.log
  fi
else
  echo "❌ Build failed. Checking for errors..."
  tail -n 50 logs/nextjs-dev.log
fi

