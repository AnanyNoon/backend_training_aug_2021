FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /src
EXPOSE 8080

# necessary for profiler
RUN apt-get update && apt-get install -y curl perl-modules procps && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==1.0.5
RUN poetry config virtualenvs.create false
COPY poetry.lock /src/
COPY pyproject.toml /src/
RUN poetry install

COPY . /src
RUN cd /src && python setup.py develop

RUN chmod +x /src/bin/run.sh

CMD ["/src/bin/run.sh"]
