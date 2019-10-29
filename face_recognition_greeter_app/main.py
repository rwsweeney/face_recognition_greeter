from face_reco import start_video
import sys

# Add arg parser to create mode for startup

ip = "rtsp://192.168.43.1:8080/h264_ulaw.sdp"

try:
    start_video(ip, sys.argv[1])
except:
    start_video(ip, sys.argv[0])