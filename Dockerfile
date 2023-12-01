FROM python:3.11-slim

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV OPENAI_API_KEY='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'

RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /apps
COPY . /apps

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "apps.main:app"]
