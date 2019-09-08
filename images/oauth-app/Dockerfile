FROM python:latest

RUN apt-get update && apt-get upgrade -y 
RUN pip install gunicorn requests flask requests_oauth2 pyyml
RUN mkdir /opt/oauth-proxy

COPY src/ /opt/oauth-proxy

WORKDIR /opt/oauth-proxy/

CMD ["gunicorn", "wsgi:app", "-b", "0.0.0.0:80"]
