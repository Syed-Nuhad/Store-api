FROM python:3.10

# Expose the default Flask port
EXPOSE 5000

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy app files
COPY . .

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Run the Flask app
CMD ["python", "app.py"]
