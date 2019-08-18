#
# Tesseract 4 OCR Runtime Environment - Docker Container
#

FROM ubuntu:19.04

LABEL description="Container using Ubuntu 19.04 to run Tesseract 4.1.0"
LABEL version="0.1"
LABEL author="David Valpey"
LABEL email="david.valpey@viqtordavis.com"

RUN mkdir /home/work
WORKDIR /home/work

RUN apt-get update && apt-get install -y software-properties-common && add-apt-repository -y ppa:alex-p/tesseract-ocr
RUN apt-get update && apt-get install -y tesseract-ocr-all && apt-get autoremove && apt-get clean

CMD /bin/bash