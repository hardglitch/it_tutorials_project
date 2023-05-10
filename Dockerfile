FROM uvicorn-fastapi-basic
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./app ./app
COPY ./privatekey.key .
COPY ./certificate.pem .
COPY ./.env_docker ./.env
CMD uvicorn app.main:app --host 0.0.0.0 --port 443 --ssl-keyfile ./privatekey.key --ssl-certfile ./certificate.pem --reload