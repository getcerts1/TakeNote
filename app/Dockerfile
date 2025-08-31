FROM python:3.13-slim

# Install dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*


WORKDIR /opt

COPY app/requirements.txt .

#Install Python dependencies removing pip wheels
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 5000


CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
