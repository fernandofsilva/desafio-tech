# Image base
FROM python:latest

LABEL maintainer="Fernando Silva <fernandosk8@gmail.com>"

# Copy requirements.txt
COPY ./requirements.txt /app/requirements.txt

# Copy data files
COPY data ./app/

# Set working directory
WORKDIR /app

## Upgrade pip
RUN pip3 install --upgrade pip

# Install
RUN pip install -r requirements.txt

# Copy all files to app folder
COPY . /app

ENTRYPOINT ["python"]

CMD ["app.py"]