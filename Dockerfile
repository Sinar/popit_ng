FROM django:python2
MAINTAINER Sinar Monkeys <info@sinarproject.org>

RUN apt-get update && \
    apt-get upgrade -qy && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

# Copy all code over for production deployment
# Dev will use override to VOLUME mount local code
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN ./manage.py migrate

CMD ./manage.py runserver 0.0.0.0:8000
