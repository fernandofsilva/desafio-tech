FROM python:latest

LABEL maintainer="Fernando Silva <fernandosk8@gmail.com>"

## Install Python3 general packages.
RUN pip3 install --upgrade pip

# Copy requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

# Copy data files
COPY data ./app/

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["python"]

CMD ["app.py"]