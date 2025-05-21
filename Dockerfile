# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . .

# Set environment variable so Python outputs logs immediately
ENV PYTHONUNBUFFERED=1

# Command to run the app
CMD ["flask", "run", "--host=0.0.0.0"]
