FROM python:3.9-slim
WORKDIR /app

# Copy requirements to the container and install requirements.txt
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy all the app code to the container
COPY . .

# Port for localhost
EXPOSE 8001

# Commando to initialize the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
