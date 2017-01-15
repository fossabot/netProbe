# Docker file for a logstash server to be bound to the server
# 
# Time-stamp: <2017-01-15 20:09:02 alex>
#
# docker build -t piprobe-logstash .
# docker run -d -p 55514:55514/udp -p 55514:55514/tcp piprobe-logstash

FROM logstash

MAINTAINER Alex <achauvinhameau@gmail.com>

EXPOSE 55514/udp
EXPOSE 55514/tcp

COPY logstash.conf /logstash.conf

CMD ["-f", "/logstash.conf"]
