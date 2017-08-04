FROM python:2.7

MAINTAINER anshuman.bhartiya@gmail.com

RUN mkdir /opt/cloudflare-enum
WORKDIR /opt/cloudflare-enum

RUN pip install requests
RUN pip install bs4

ADD cloudflare_enum.py /opt/cloudflare-enum/

ENTRYPOINT ["./cloudflare_enum.py"]