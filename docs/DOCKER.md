Docker test client
==================

image
-----

in the docker directory, Dockerfile based on the debian jessie version

docker build -t netprobe .

docker run --name redis -d redis
docker run --name pi01 --link redis:redis -it netprobe bash


Docker server
==================

docker build -t piprobe-srv .

docker run --name piprobe-srv -p 5000:5000 -p 5201:5201/udp -it piprobe-srv bash
