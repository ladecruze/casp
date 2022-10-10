FROM python:3-alpine
ADD . /CASP
WORKDIR /
ENV FLASK_APP=CASP
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk update 
RUN apk add gcc musl-dev libffi-dev openssl-dev libpq-dev python3-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000

CMD [ "flask","run","-p","8000" ]
