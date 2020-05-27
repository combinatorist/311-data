FROM python:3.7-slim

RUN apt-get update && \
    apt-get install -yq \
      python3 \
      python3-dev \
      gcc \
      g++ \
      gfortran \
      musl-dev && \
    pip install --upgrade pip

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY .env* src/ /app/

WORKDIR /app/src

CMD ["python", "app.py"]
