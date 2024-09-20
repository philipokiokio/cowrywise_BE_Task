# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Make port 6969 available to the world outside this container
EXPOSE 6970

# Define environment variable
ENV PYTHONPATH=/app

# If you still intend to use `make run_server` (ensure make is installed)
# Install make
RUN apt-get update && apt-get install -y make && rm -rf /var/lib/apt/lists/*



# Run FastAPI app with Uvicorn
CMD ["make", "prod_server"]
