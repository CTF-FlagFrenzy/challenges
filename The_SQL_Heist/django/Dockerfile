FROM python:3

COPY django/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . code
WORKDIR /code

EXPOSE 8002

ENTRYPOINT ["python", "django/manage.py"]
CMD ["runserver", "0.0.0.0:8002"]
