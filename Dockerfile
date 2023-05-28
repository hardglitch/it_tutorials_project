FROM python:3.11
WORKDIR /code
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./app ./app
COPY ./migrations ./migrations
COPY ./alembic.ini .
COPY ./.env ./.env
COPY ./setup.py .
RUN python setup.py install
RUN alembic upgrade head
WORKDIR ./app
ENTRYPOINT gunicorn main:app --workers 1 -worker-class uvicorn.workers.UvicornWorker
