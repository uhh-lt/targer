# Use an official Python runtime as a parent image
FROM python:3.5

# Add all Data
ADD . /

# Set the working directory to /
WORKDIR /

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

RUN git clone https://github.com/UKPLab/emnlp2017-bilstm-cnn-crf.git

RUN mv backend.py emnlp2017-bilstm-cnn-crf/ && mv Model.py emnlp2017-bilstm-cnn-crf/ && mv ModelNewES.py emnlp2017-bilstm-cnn-crf/ && mv ModelNewWD.py emnlp2017-bilstm-cnn-crf/

RUN mv models/* emnlp2017-bilstm-cnn-crf/models/

RUN mv -f BiLSTM.py emnlp2017-bilstm-cnn-crf/neuralnets/

RUN mkdir emnlp2017-bilstm-cnn-crf/lstm

RUN git clone https://github.com/achernodub/bilstm-cnn-crf-tagger.git emnlp2017-bilstm-cnn-crf/lstm

# Make port 6000 available to the world outside this container
EXPOSE 6000

WORKDIR /emnlp2017-bilstm-cnn-crf

# Run app.py when the container launches
CMD ["python3", "backend.py"]









