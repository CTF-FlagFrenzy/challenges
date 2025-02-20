FROM python:3

COPY django/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . code
WORKDIR /code

EXPOSE 80

ENTRYPOINT ["python", "django/manage.py"]
RUN python django/manage.py migrate
CMD ["runserver", "0.0.0.0:80"]

