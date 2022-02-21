FROM python:3.8.10

RUN pip install psycopg2-binary==2.9.3
RUN pip install SQLAlchemy==1.4.31
RUN pip install pandas==1.2.0
RUN pip install requests==2.22.0

ADD python /source-code/

WORKDIR /source-code/



CMD ["python", "start.py"]
