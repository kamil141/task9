FROM python:3.7-alpine3.15
WORKDIR /usr/src/app
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
COPY . /usr/src/app/
EXPOSE 8000
CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:8000", "main:app"]
