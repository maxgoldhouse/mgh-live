FROM alpine:3.10

RUN apk add --update --no-cache \
    bash \
    python && \
    python -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip install --upgrade pip setuptools && \
    rm -r /root/.cache && \
    pip install jinja2

CMD ["bash", "./scripts/NEW-en-scripts/deploy.sh"]
