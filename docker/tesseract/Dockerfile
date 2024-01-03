#
# Tesseract 4 OCR Runtime Environment - Docker Container
#

FROM ubuntu:20.04

LABEL description="Container using Ubuntu 20.04 to run Tesseract 4.1.0"
LABEL version="0.1"
LABEL author="David Valpey"

RUN mkdir /home/work
WORKDIR /home/work

RUN apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-nld tesseract-ocr-eng && apt-get autoremove && apt-get clean

CMD /bin/bash