import rtsp
import time

try:
    with rtsp.Client(rtsp_server_uri='rtsp://174.0.247.195:554/1/') as client:
        _image = client.read()
        
        print(_image)
        # if client is None:
        #     print(True)
        # else:
        #     print(False)

        _image.save('1.jpg')
except Exception as ex:
    print(ex)
