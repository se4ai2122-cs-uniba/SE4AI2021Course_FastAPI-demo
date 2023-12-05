FROM python:3.10
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY . /fastAPIapp
WORKDIR /fastAPIapp
EXPOSE 55000
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "55000"]
