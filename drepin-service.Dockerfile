## Builds a Docker image for the Service
## To srat the service in a docker, run
##   docker run -it --rm -p 8080:8080 --name drepin-service  gcr.io/drepin-project/drepin-service
## Use the following URL to display the SWAGGER UI in the client 
##   http://10.128.0.20:8080/v1/ui/
##
FROM centos:7
LABEL maintainer="Dmitriy Repin <drepin@hotmail.com>"

USER 0

# Extra Packages for Enterprise Linux (EPEL) repository. 
RUN yum install -y epel-release

## Python 3.4 (python3.4, pip3.4)
RUN yum install -y python34 python34-pip

COPY src/requirements.txt /headless/requirements.txt

RUN pip3 install --no-cache-dir -r /headless/requirements.txt

EXPOSE 8080

ENV PYTHONPATH="/app/src:/app/src/generated"

USER 1000

#---------------------------------------------------------
WORKDIR /app
CMD python3 ./src/main.py
# CMD gunicorn main:app -w $NUM_WORKERS -k gevent -b 0.0.0.0:8080 --access-logfile -
