# Use Python 3.13 slim image (multi-arch, works on Raspberry Pi ARM)
FROM python:3.13-slim-bullseye

# Set working directory
WORKDIR /app

# Install system dependencies if needed (none currently)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Install the package itself (makes weather-fetch available)
RUN pip install .

# Default command
CMD ["weather-fetch"]