FROM python 

WORKDIR /app

RUN pip install --upgrade pip

COPY . /app

CMD ["python", "main.py"]