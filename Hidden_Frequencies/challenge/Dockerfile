# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy necessary files
COPY server.py .
COPY challenge_image.png /app/static/

# Install dependencies
RUN pip install flask

# Expose port 5000
EXPOSE 8006

# Run the server
CMD ["python", "server.py"]