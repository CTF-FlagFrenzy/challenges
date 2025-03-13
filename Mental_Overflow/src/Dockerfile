FROM python:3

# Copy requirements and install dependencies
COPY src/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire codebase into the container
COPY . /code
WORKDIR /code
EXPOSE 80
# Ensure the script is executable
RUN chmod +x src/script.py

# Set the entrypoint to run script.py
ENTRYPOINT ["python", "src/file_server.py"]