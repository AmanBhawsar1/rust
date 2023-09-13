# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory to /app
WORKDIR /home/aman
# Copy the current directory contents into the container at /app
COPY . .

# Install Streamlit and any other dependencies you need
RUN pip install streamlit

# Make port 8051 available to the world outside this container
EXPOSE 8051

# Define environment variable
ENV NAME StreamlitApp

# Run streamlit when the container launches
CMD ["streamlit", "run", "/home/aman/image_processing.py","--server.port", "8051", "--server.host", "localhost"]
