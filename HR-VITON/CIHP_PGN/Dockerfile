# Use a lightweight Python base image
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Install required system packages
RUN apt-get update && \
    apt-get install -y wget build-essential libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    chmod +x Miniconda3-latest-Linux-x86_64.sh && \
    ./Miniconda3-latest-Linux-x86_64.sh -b -p /opt/miniconda && \
    rm Miniconda3-latest-Linux-x86_64.sh

# Add Miniconda to PATH
ENV PATH="/opt/miniconda/bin:$PATH"

# Create a Conda environment with Python 3.7
RUN conda create -n myenv python=3.7 -y && \
    conda init bash

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

# Set the working directory in the container
WORKDIR /app

# Copy requirements files
COPY requirement.txt /app/
COPY requirements.pip /app/

# Install MKL FFT from the Intel channel
# RUN conda install -c intel mkl_fft

# # Install other dependencies in the Conda environment
RUN conda run -n myenv pip install --no-cache-dir -r requirement.txt && \
    conda run -n myenv pip install --no-cache-dir -r requirements.pip

# Copy the script into the container
COPY api_script.py /app/

# Run the script when the container launches
CMD ["conda", "run", "-n", "myenv", "python", "/app/api_script.py"]
