FROM python
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
ADD . /app/
CMD ["python","-u","booking.py"]
