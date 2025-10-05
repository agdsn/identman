FROM python:3.13-slim-trixie

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

RUN curl --proto '=https' --tlsv1.2 -LsSf https://github.com/astral-sh/uv/releases/download/0.8.15/uv-installer.sh | sh \
    && mv $HOME/.local/bin/uv /usr/local/bin/


WORKDIR /opt/identman
COPY --link pyproject.toml /opt/identman



WORKDIR /opt/identman
RUN uv pip install --system . --group prod
COPY --link identman/ /opt/identman/identman
WORKDIR /opt/identman
EXPOSE 5000
CMD ["gunicorn", "identman.main:app", "-w 4", "-k", "uvicorn_worker.UvicornWorker"]