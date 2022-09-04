FROM python:3.9.13

WORKDIR /scripts

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY *.py .

ENV MAIN_PY="main.py"

CMD "python ${MAIN_PY}"
