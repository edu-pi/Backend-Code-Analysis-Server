FROM python:3.11-alpine

WORKDIR /home/visualize
RUN pip install poetry

COPY pyproject.toml /home/visualize
COPY poetry.lock /home/visualize

COPY app /home/visualize/app

RUN poetry install --no-root

EXPOSE 8000

ENTRYPOINT [ "poetry" ,"run", "uvicorn", "app.route:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]