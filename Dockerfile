# Use Python 3.13 slim image (multi-arch, works on Raspberry Pi ARM)
FROM python:3.13-slim-bullseye

# Set working directory
WORKDIR /app

# Install system dependencies if needed (none currently)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     && rm -rf /var/lib/apt/lists/*

# Copy pyproject config first for better caching
COPY pyproject.toml ./

# Copy the project sources
COPY . .

# Install Python dependencies and the package
RUN pip install --no-cache-dir .

# Default command
CMD ["weather-fetch"]