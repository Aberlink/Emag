FROM python:3.11-slim

RUN mkdir -p /home/blog_app
WORKDIR /home/blog_app

COPY . /home/blog_app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


EXPOSE 8000


