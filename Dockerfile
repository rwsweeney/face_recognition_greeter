FROM        python:3.6

COPY        ./face_recognition_greeter_app ./conf /opt/app/

RUN         pip install -r /opt/app/requirements.txt \
            && mkdir -p ~/.aws \
            && cp /opt/app/config /opt/app/credentials ~/.aws/
