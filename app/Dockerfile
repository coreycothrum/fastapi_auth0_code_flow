FROM python:3.11

WORKDIR /fastapi_app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/fastapi_app

COPY ../requirements.txt                     /fastapi_app/requirements.txt
RUN  pip install --no-cache-dir --upgrade -r /fastapi_app/requirements.txt

VOLUME ["/fastapi_app/app" ]
VOLUME ["/fastapi_app/fastapi_auth0_code_flow" ]

ENTRYPOINT [ "python3", "/fastapi_app/app/main.py" ]
