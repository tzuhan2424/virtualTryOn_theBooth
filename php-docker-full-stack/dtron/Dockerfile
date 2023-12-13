# Use a lightweight Python base image
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install required packages in one layer
RUN apt-get update && \
    apt-get install -y wget build-essential git-all && \
    apt-get install -y libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    chmod +x Miniconda3-latest-Linux-x86_64.sh && \
    ./Miniconda3-latest-Linux-x86_64.sh -b -p /opt/miniconda && \
    rm Miniconda3-latest-Linux-x86_64.sh

ENV PATH="/opt/miniconda/bin:$PATH"

# Initialize Conda in bash config
RUN /opt/miniconda/bin/conda init bash

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt files into the container
COPY requirements.txt /app/
COPY requirements2.txt /app/

# Install dependencies and detectron2
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements2.txt && \
    git clone https://github.com/sking115422/detectron2.git && \
    cd detectron2 && \
    pip install -e .

# Copy the script into the container
COPY api_script.py /app/

# Run the script when the container launches
CMD ["python", "/app/api_script.py"]
