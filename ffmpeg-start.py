import subprocess

# Command to stream camera feed using FFmpeg (replace '/dev/video0' with your camera device)
ffmpeg_command = [
    'ffmpeg',
    '-f', 'v4l2',
    '-framerate', '30',
    '-video_size', '640x480',
    '-i', '/dev/video0',
    '-c:v', 'libx264',
    '-preset', 'ultrafast',
    '-tune', 'zerolatency',
    '-f', 'mpegts',
    'udp://0.0.0.0:5001'  # Change the URL/port as needed
]

# Launch FFmpeg subprocess
ffmpeg_process = subprocess.Popen(ffmpeg_command)

# Wait for process to finish (optional)
ffmpeg_process.wait()
