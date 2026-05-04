# TODO: Write a production-ready Dockerfile
#
# All of these are tested by the grader:
#
# [ ] Multi-stage build (2+ FROM instructions)
# [ ] Base image: python:3.14-slim (pinned version, no :latest)
# [ ] Copy requirements.txt and pip install BEFORE copying source code (layer caching)
# [ ] Run as a non-root USER
# [ ] EXPOSE 8080
# [ ] HEALTHCHECK instruction
# [ ] No hardcoded secrets (no ENV PASSWORD=..., no ENV SECRET_KEY=...)
# [ ] Final image under 200MB
#
# Start command: uvicorn src.app:app --host 0.0.0.0 --port 8080
FROM python:3.14-slim AS build
WORKDIR /build
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --target=/deps --no-cache-dir -r requirements.txt



FROM python:3.14-slim

LABEL org.opencontainers.image.title="SDyPP - excersice 1"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.source="https://github.com/EViani/exercise-01-node-registry"
LABEL org.opencontainers.image.authors="Esteban Viani <eviani94@hotmail.com>"

WORKDIR /app

RUN groupadd -r appgroup && useradd -r -g appgroup appuser

COPY --from=build --chown=appuser:appgroup /deps /deps 

COPY --chown=appuser:appgroup . .
USER appuser

ENV PYTHONPATH=/app:/deps
ENV PATH="/deps/bin:$PATH"

EXPOSE 8080
HEALTHCHECK --interval=30s CMD "curl -f http://localhost:8080/health" || exit 1

CMD [ "uvicorn","src.app:app","--host", "0.0.0.0", "--port", "8080", "--reload"]