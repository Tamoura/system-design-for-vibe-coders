# labs/m14/Dockerfile
# From aiapps/labkit: docker build -f labs/m14/Dockerfile --target runtime -t najm-desk:dev .
# Pin the base: an exact tag, in production its digest (image@sha256:...).
ARG PYTHON_IMAGE=python:3.11.9-slim-bookworm

FROM ${PYTHON_IMAGE} AS build
WORKDIR /build
COPY labs/m14/requirements.txt .
RUN python -m venv /venv && /venv/bin/pip install --no-cache-dir -r requirements.txt

# Development only: the offline stand-in for the model API. Never deploy this stage.
FROM ${PYTHON_IMAGE} AS mock
WORKDIR /app
COPY --from=build /venv /venv
COPY labkit ./labkit
ENV PATH="/venv/bin:$PATH"
CMD ["python", "-m", "labkit.mock_server", "--host", "0.0.0.0", "--port", "8787"]

# The last stage is what `docker build` ships: no compiler, no tests, no mock, no key.
FROM ${PYTHON_IMAGE} AS runtime
WORKDIR /app
RUN useradd --system --uid 10001 app
COPY --from=build /venv /venv
COPY labkit/data/policies ./labkit/data/policies
COPY labs/m14/prompts ./labs/m14/prompts
COPY labs/m14/app.py ./labs/m14/app.py
ARG GIT_SHA=dev
ENV PATH="/venv/bin:$PATH" PYTHONUNBUFFERED=1 GIT_SHA=${GIT_SHA}
# Numeric, so an orchestrator can check that the process is not root.
USER 10001
EXPOSE 8000
CMD ["uvicorn", "--app-dir", "labs/m14", "app:app", "--host", "0.0.0.0", "--port", "8000"]
