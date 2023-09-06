FROM python:3.11-slim-bookworm
#docker file to build a thin image for the fastapi on main.py
#install the requirements
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main.py .
COPY models.py .
ARG PORT=8000
#expose the port
EXPOSE ${PORT}

ENV UVICORN_PORT ${PORT}

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
