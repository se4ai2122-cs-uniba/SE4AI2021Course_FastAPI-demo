FROM python:3.10-slim

WORKDIR /mnt/locust
RUN pip install locust

EXPOSE 8089

CMD ["locust", "--host", "${TARGET_HOST}"]