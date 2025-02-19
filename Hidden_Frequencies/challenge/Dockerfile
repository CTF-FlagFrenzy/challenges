# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy necessary files
COPY server.py .
COPY hidden_frequencies.bmp .

# Install dependencies
RUN pip install flask

# Expose port 5000
EXPOSE 5000

# Run the server
CMD ["python", "server.py"]
