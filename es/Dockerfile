FROM elasticsearch:6.4.2

ADD . /usr/share/elasticsearch

RUN mkdir data/myindex
RUN chown -R elasticsearch:elasticsearch ./data
RUN echo 'path.data: /usr/share/elasticsearch/data/myindex' >> config/elasticsearch.yml
RUN chmod a+x /usr/share/elasticsearch/script.sh
RUN curl https://cloud.mafiasi.de/index.php/s/33pxcy2kBqTsc7E/download > MD5.sum
RUN curl https://cloud.mafiasi.de/index.php/s/LsKq4dd4ztaJPci/download > index.zip
RUN unzip ./index.zip -d /usr/share/elasticsearch/data/myindex


ENTRYPOINT /usr/share/elasticsearch/script.sh

