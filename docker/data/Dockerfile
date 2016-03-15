FROM alpine

ENV POPIT_DATA /usr/src/app
ENV PGDATA /var/lib/postgresql/data

RUN mkdir -p $POPIT_DATA

# explicitly set user/group IDs
# user / group postgres already exist in default alpine
# RUN groupadd -r postgres --gid=999 && useradd -r -g postgres --uid=999 postgres

RUN mkdir -p $PGDATA && chown -R postgres:postgres $PGDATA

VOLUME ["/usr/src/app", "/var/lib/postgresql/data"]

CMD tail -f /dev/null
