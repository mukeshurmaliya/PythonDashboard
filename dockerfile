# Use an official Python image as base
FROM python:3.12.1

# Set the working directory in the container
WORKDIR /app

# Copy requirements file to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the Dash application port
EXPOSE 8050

# Command to run the Dash app
CMD ["python", "RKTDashoardDV32.py"]
