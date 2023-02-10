FROM python:slim

WORKDIR /kaizen

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt && rm -f requirements.txt

COPY . .

CMD python -m kaizen