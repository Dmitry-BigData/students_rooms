FROM python

RUN pip install poetry

WORKDIR /app

COPY /pyproject.toml .
COPY /poetry.lock .
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

RUN mkdir "query_results"

ENTRYPOINT ["poetry", "run"]

COPY /python .

CMD ["python", "main.py"]
