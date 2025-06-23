FROM python:3.13

COPY ./requirements.txt /
RUN pip install --upgrade pip uwsgi
RUN pip install -r /requirements.txt

ARG UID=1000
ARG GID=1000

RUN groupadd -g "${GID}" admin \
    && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" admin

COPY ./start.sh /

WORKDIR /app
USER admin

EXPOSE 80
VOLUME [ "/data", "/app" ]

ENTRYPOINT [ "/start.sh" ]
CMD [ "uwsgi" ]
