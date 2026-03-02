#!/bin/bash

echo "=== System Resources Check ==="
echo ""

echo "Memory Usage:"
free -h

echo ""
echo "Disk Space:"
df -h /

echo ""
echo "CPU Load:"
uptime

echo ""
echo "Running Node.js Processes:"
ps aux | grep node | grep -v grep

echo ""
echo "Port Usage:"
netstat -tulpn | grep LISTEN

echo ""
echo "=== End of System Resources Check ==="

