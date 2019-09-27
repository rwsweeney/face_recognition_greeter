from face_reco import start_video

# Add arg parser to create mode for startup

ip = "rtsp://192.168.43.1:8080/h264_ulaw.sdp"

start_video(ip)
