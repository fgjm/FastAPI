FROM python:3.9-alpine3.18
COPY . .
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt
EXPOSE 5003
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5003"]
