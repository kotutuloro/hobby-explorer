FROM python:3.13
 
WORKDIR /backend
 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1
 
# install system dependencies
RUN apt-get update \
  && apt-get -y install postgresql \
  && apt-get clean
 
# install python dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
COPY ./Pipfile ./Pipfile.lock ./
RUN pipenv install -d --system --deploy
 
COPY . .

CMD ["fastapi", "run", "app/main.py", "--port", "80"]
 