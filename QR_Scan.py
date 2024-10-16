import cv2
import numpy as np
from pyzbar.pyzbar import decode


#program open's camera to it will scan the selected QR code you have on hand & will take you to website on that scanned QR.
#for the momment I only have it to open camera & detect the QR - won't take you to any other website (unless it does?) 

#V2 - when scanning QR code, it will track the URL on screen real time & will give link in output box...

# next version - adding a GUI to simplify the user experince when scanning QR code...

def qr_code_scanner():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        for barcode in decode(frame):
            my_data = barcode.data.decode('utf-8')
            print(f"QR Code data: {my_data}")

            # Draw a rectangle around the detected QR Code
            points = barcode.polygon
            if len(points) > 4:
                hull = cv2.convexHull(np.array([points for point in points],dtype=np.float32))
                points = hull.tolist()
            n = len(points)
            for j in range(n):
                cv2.line(frame, tuple(points[j]), tuple(points[(j + 1) % n]), (255, 0, 0), 3)

            # Print the QR code data on the frame
            x ,y, w, h = barcode.rect
            cv2.putText(frame,my_data, (x,y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 225, 0), 2)
        cv2.imshow('QR Code Scanner', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

qr_code_scanner()
qr_code_scanner()
