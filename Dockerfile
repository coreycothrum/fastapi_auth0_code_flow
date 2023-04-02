FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN  pip install --no-cache-dir --upgrade  build

VOLUME     [ "/src_code" ]
WORKDIR       /src_code
ENTRYPOINT [ "python3", "-m", "build" ]
