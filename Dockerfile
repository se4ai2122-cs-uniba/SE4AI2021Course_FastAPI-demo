FROM python:3.10
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY . /fastAPIapp
WORKDIR /fastAPIapp
EXPOSE 55000
CMD ["fastapi", "run", "app/api.py"]
