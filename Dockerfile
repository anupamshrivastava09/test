FROM python:3.8-alpine
RUN mkdir -p /Czentrix/apps/tts_fastapi
COPY . /Czentrix/apps/
WORKDIR /Czentrix/apps/tts_fastapi
ENV venv="/Czentrix/apps/tts_fastapi/venv"

RUN python3 -m venv $venv
RUN $venv/bin/pip install --upgrade pip
RUN $venv/bin/pip install -r tts_requirement.txt

CMD ["/Czentrix/apps/tts_fastapi/venv/bin/gunicorn", "-w", "3", "-k", "uvicorn.workers.UvicornWorker", "fastapi_tts:app", "--bind", "0.0.0.0:8000"]
