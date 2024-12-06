FROM python:3.11-alpine

WORKDIR /home/assist
RUN pip install poetry

COPY pyproject.toml /home/assist
COPY poetry.lock /home/assist
COPY .env /home/assist

COPY app /home/assist/app

RUN poetry install --no-root

EXPOSE 8001

ENTRYPOINT [ "poetry" ,"run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]