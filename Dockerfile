# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the non-interactive environment variable (this helps with some installations)
ENV DEBIAN_FRONTEND noninteractive

# Update and install system and Tkinter dependencies
RUN apt-get update && apt-get install -y \
    python3-tk \
    tk \
    x11-apps \
    libx11-6 \
    libxss1 \
    libxft2 \
    libxext6 \
    libxt6 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Run snake_game.py when the container launches
CMD ["python", "./src/snake_game.py"]
