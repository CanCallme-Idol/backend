FROM python:3
WORKDIR /backend

## Install packages
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx

## Copy all src files
COPY . .

CMD [ "python3","manage.py","runserver","0.0.0.0:8000"]

## Run the application on the port 8080
EXPOSE 8000