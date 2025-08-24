FROM python:3.13-alpine

# Install dependencies
RUN apk update && apk upgrade && apk add --no-cache gcc musl-dev linux-headers

WORKDIR /opt

COPY requirements.txt .

#Install Python dependencies removing pip wheels
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000


CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
