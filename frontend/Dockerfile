# Use an official Python runtime as a parent image
FROM tiangolo/uwsgi-nginx-flask:python3.7

# Add all Data
ADD . /

# Set the working directory to /
WORKDIR /

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

RUN python -m spacy download xx

RUN python -m pip install "msgpack<0.6.0"

ENV LISTEN_PORT 6001
ENV UWSGI_INI /uwsgi.ini
ENV STATIC_PATH /static

# Make port 6001 available to the world outside this container
EXPOSE 6001

# Run app.py when the container launches
#CMD ["python3", "frontend.py"]









