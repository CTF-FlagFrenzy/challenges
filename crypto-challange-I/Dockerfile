FROM httpd:latest

# Install Python
RUN apt-get update && apt-get install -y python3

# Copy the startup script and Python script
COPY ./start.sh /usr/local/bin/start.sh
COPY ./script.py /usr/local/bin/script.py

# Make the startup script executable
RUN chmod +x /usr/local/bin/start.sh

# Set the entrypoint to the startup script
ENTRYPOINT ["/usr/local/bin/start.sh"]

EXPOSE 80