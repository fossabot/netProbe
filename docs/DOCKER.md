Docker test client
==================

image
-----

in the docker directory, Dockerfile based on the debian jessie version

docker build -t netprobe .

redis should be running on the host

docker run -d netprobe
