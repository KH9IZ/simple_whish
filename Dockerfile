FROM python:3.12

WORKDIR /simple_whish
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY forms.py main.py models.py .

VOLUME /var/db/simple_whish
EXPOSE 80/tcp

CMD ["gunicorn", "--bind=0.0.0.0:80", "main:app"]
