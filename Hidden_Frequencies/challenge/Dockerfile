# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy necessary files
COPY script.py .
COPY hidden_frequencies.bmp .

# Install dependencies
RUN pip install flask

# Expose port 5000
EXPOSE 80

# Run the server
CMD ["python", "script.py"]
