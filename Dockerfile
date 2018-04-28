FROM some-registry.com/some-linux-image:1.0

RUN pip install flask flask_restful statsd
COPY files/jadder.py /
