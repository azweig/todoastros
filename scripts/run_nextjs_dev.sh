#!/bin/bash

echo "Starting Next.js in development mode for debugging..."

# Kill any existing Node.js processes
echo "Stopping any running Node.js processes..."
pkill -f node || true

# Create logs directory if it doesn't exist
mkdir -p logs

# Start Next.js in development mode with increased logging
echo "Starting Next.js development server..."
NODE_OPTIONS="--max-old-space-size=1024" npm run dev > logs/nextjs-dev.log 2>&1 &

echo "Waiting for Next.js to start..."
sleep 10

# Check if the application is running
if lsof -i:3000 | grep LISTEN > /dev/null; then
  echo "✅ Next.js development server started successfully on port 3000"
  echo "You can access it at: http://your-server-ip:3000"
  echo "To view logs in real-time: tail -f logs/nextjs-dev.log"
else
  echo "❌ Next.js development server failed to start. Checking logs..."
  tail -n 20 logs/nextjs-dev.log
fi

