FROM python:3.12.0-slim

# Set the working directory
WORKDIR /src

# Copy the current directory contents into the container at /src
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Copy the application code
COPY app/ /src/app/
COPY tests/ /src/tests/
COPY .env /src/.env

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]