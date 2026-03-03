#!/bin/bash

# This is the startup script inside Docker environment
# Start the Uvicorn server
echo "Starting the uvicorn server"
exec uvicorn --no-server-header --host 0.0.0.0 --log-level info app.main:app
