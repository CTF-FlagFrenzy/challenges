FROM python:3

COPY . code
WORKDIR /code
RUN pip install --no-cache-dir -r flask_app/requirements.txt
EXPOSE 80

ENTRYPOINT ["python", "flask_app/app.py"]
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]