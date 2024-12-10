FROM python:3.12.4-alpine3.19
LABEL maintainer="42Barcelona"

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./scripts /scripts
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false

RUN pip install --upgrade pip setuptools && \
	apk add --update --no-cache \
	postgresql-client \
	libffi-dev \
	gettext \
	build-base && \
	apk add --update --no-cache --virtual .tmp-build-deps \
	build-base \
	postgresql-dev \
	musl-dev \
	zlib \
	zlib-dev \
	linux-headers \
	python3-dev \
	libuv-dev \
	libffi-dev \
	openssl-dev && \
	pip install -r /tmp/requirements.txt && \
	if [ $DEV = "true" ]; \
	then  pip install -r /tmp/requirements.dev.txt ; \
	fi && \
	rm -rf /tmp && \
	apk del .tmp-build-deps && \
	adduser \
	--disabled-password \ 
	--no-create-home \
	django-user && \
	mkdir -p /vol/web/media \
	mkdir -p /vol/web/static \
	mkdir -p /vol/log && \
	chown -R django-user:django-user /vol /app && \
	chmod -R 777 /vol /app && \
	chmod -R +x /scripts

ENV PATH="/scripts:$PATH"

USER django-user

RUN rm -rf /vol/cache/__pycache__/*


CMD ["run.sh"]