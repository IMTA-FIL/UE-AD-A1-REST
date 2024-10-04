FROM python
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
ADD . /app/
CMD ["watchmedo", "auto-restart", "--patterns=*.py", "--recursive", "--", "python", "-u", "movie.py"]
