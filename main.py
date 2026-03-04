import cv2 as cv
import sys
import mediapipe as mp
import numpy
import time
from mediapipe.tasks.python.vision import drawing_utils
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
latest_result = None


def result_callback(result, output_image: mp.Image, timestamp_ms: int):
    global latest_result
    latest_result=result
    print('hand landmarker rasult: {}'.format(result))
    
def audio_set():
    devices =AudioUtilities.GetSpeakers()
    interface = devices.EndpointVolume
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    volRange = volume.GetVolumeRange()
    minVol = volRange[0]
    maxVol = volRange[1]
    return volume, minVol, maxVol


def main():
    
    video= cv.VideoCapture(0,cv.CAP_MSMF)

    video.set(cv.CAP_PROP_FRAME_WIDTH,640)
    video.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
    video.set(cv.CAP_PROP_FPS,24)

    BaseOptions = mp.tasks.BaseOptions
    HandLandmarker = mp.tasks.vision.HandLandmarker
    HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
    VisionRunningMode= mp.tasks.vision.RunningMode
    HandLandmarkerConnections = mp.tasks.vision.HandLandmarksConnections
    
    volume, minVol, maxVol =audio_set()

    options = HandLandmarkerOptions(
        base_options =BaseOptions(model_asset_path='D:\Curso python\Portafolio\hand_landmarker.task'),
        running_mode = VisionRunningMode.LIVE_STREAM,
        result_callback = result_callback,
        num_hands= 1,
        min_hand_detection_confidence =0.5
        )
    
    detector = HandLandmarker.create_from_options(options)

    if video.isOpened() == False:
        sys.exit("Error al abrir la cámara")
    
    while True:
        success, img = video.read()

        if success == False or img is None:
            print("Cámara detectada pero sin señal... reintentando")
            cv.waitKey(100)
            continue

        img = cv.flip(img,1)

        img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)


        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
        mp_draw = drawing_utils
        mp_hands = HandLandmarkerConnections
        ActualTime= time.time()*1000
        detector.detect_async(mp_image,int(ActualTime))

        if latest_result and latest_result.hand_landmarks:

            h = mp_image.height
            w = mp_image.width

    

            for hand_landmarks_proto in latest_result.hand_landmarks:
                mp_draw.draw_landmarks(
                    img,                                
                    hand_landmarks_proto,               
                    mp_hands.HAND_CONNECTIONS,          
                    mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2), 
                    mp_draw.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)  
                )

                thumb = hand_landmarks_proto[4]
                x1,y1 = int(thumb.x * w), int(thumb.y * h)

                index = hand_landmarks_proto[8]
                x2,y2 = int(index.x*w), int(index.y * h)

                cx, cy = (x1 +x2)//2, (y1 + y2) // 2

                distance = numpy.hypot(x2 -x1, y2-y1)

                cv.circle(img, (x1, y1), 10, (255, 0, 255), cv.FILLED) # Morado
                cv.circle(img, (x2, y2), 10, (255, 0, 255), cv.FILLED)
                
                cv.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                # Dibujamos un círculo en el centro que cambie de color si están muy cerca
                if distance < 30:
                    cv.circle(img, (cx, cy), 10, (0, 255, 0), cv.FILLED) # Verde si se tocan


                vol = numpy.interp(distance, [0,100], [minVol, maxVol])
                volume.SetMasterVolumeLevel(vol, None)      
        cv.imshow("Prueba_video",img)

       
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    video.release()
    cv.destroyAllWindows()

main()
