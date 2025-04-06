# File: Dockerfile

FROM debian:bullseye-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    wget \
    ca-certificates \
    libgl1 \
    libxrender1 \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Install FreeCAD
RUN wget https://github.com/FreeCAD/FreeCAD/releases/download/0.21.2/FreeCAD-0.21.2-Linux-x86_64.AppImage \
    -O /FreeCAD.AppImage && chmod +x /FreeCAD.AppImage && \
    /FreeCAD.AppImage --appimage-extract

ENV PATH="/squashfs-root/usr/bin:${PATH}"
ENV PYTHONPATH="/squashfs-root/usr/lib/python3.11/site-packages"

# Copy app files
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip3 install flask

# Expose port
EXPOSE 5000

# Run the Flask app
CMD ["python3", "app.py"]
