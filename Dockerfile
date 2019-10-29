FROM        python3:3

COPY        ./face_recognition_greeter_app /opt/app

RUN         pip3 install -r /opt/app/requirements.txt

ENTRYPOINT  ["python3 /opt/app/main.py"]