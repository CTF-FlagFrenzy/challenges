FROM httpd:latest

# Install Python
RUN apt-get update && apt-get install -y python3

# Copy the startup script and Python script
COPY ./start.sh /usr/local/bin/start.sh
COPY ./script.py /usr/local/bin/script.py
COPY ./requirements.txt /usr/local/bin/requirements.txt
# Make the startup script executable
RUN chmod +x /usr/local/bin/start.sh


# Update package list and install python3-venv if not already installed
RUN apt-get update && apt-get install -y python3-venv


RUN python3 -m venv /usr/local/bin/venv && \
    /usr/local/bin/venv/bin/pip install -r /usr/local/bin/requirements.txt

# Set the entrypoint to the startup script
ENTRYPOINT ["/usr/local/bin/start.sh"]

EXPOSE 80