FROM python:3

COPY flask_app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . code
WORKDIR /code

EXPOSE 8000

ENTRYPOINT ["python", "flask_app/app.py"]
CMD ["runserver", "0.0.0.0:8000"]
