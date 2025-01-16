#!/bin/sh

# Navigate to the code directory and start npm
cd /code
npm start &

# Run the inotifywait loop
while inotifywait -e close_write /uploads/; do
    sh /app/runAssembly.sh
done