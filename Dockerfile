FROM python:3.10
WORKDIR /app

COPY . /app
RUN pip3 install -r ./requirements.txt

EXPOSE 8000
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port", "8000"]
