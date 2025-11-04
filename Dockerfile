FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-dev \
    python3.10-venv \
    python3-pip \
    ngspice \
    build-essential \
    pkg-config \
    libffi-dev \
    libssl-dev \
    wget \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3.10 /usr/bin/python

RUN python -m pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

COPY . .

RUN mkdir -p /app/staticfiles \
    && mkdir -p /app/logs \
    && mkdir -p /app/memristorsimulation_app/simulation_results

EXPOSE 8000

CMD ["/bin/bash", "/app/entrypoint.sh"]