FROM python:3.9
WORKDIR /backend
COPY requirements.txt /backend
RUN pip install -r requirements.txt --no-cache-dir
COPY . /backend
CMD ["python", "manage.py", "migrate", "runserver", "0.0.0.0:8000"]