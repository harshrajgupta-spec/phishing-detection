FROM python:3.10-slim

WORKDIR /app

# Install system dependencies required by xgboost and scikit-learn
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc gfortran libatlas-base-dev liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

CMD ["python", "app.py"]
