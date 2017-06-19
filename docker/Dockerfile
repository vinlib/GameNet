FROM ubuntu:16.04
RUN apt-get update
RUN apt-get -y install git
RUN apt-get install -y python python-pip wget
RUN git clone https://github.com/vinlib/GameNet.git
WORKDIR /GameNet
RUN chmod +x server.py
CMD ["python","./server.py"]
