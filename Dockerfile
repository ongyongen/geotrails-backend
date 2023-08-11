FROM python:3.9.5
WORKDIR /app

COPY . /app
RUN pip install -r ./requirements.txt

EXPOSE 8000
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port", "8000"]
