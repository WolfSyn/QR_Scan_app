import cv2
import numpy as np
from pyzbar.pyzbar import decode


#program open's camera to it will scan the selected QR code you have on hand & will take you to website on that scanned QR.
#for the momment I only have it to open camera & detect the QR - won't take you to any other website (unless it does?) 

#Pending for further development for this app

def qr_code_scanner():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        for barcode in decode(frame):
            my_data = barcode.data.decode('utf-8')
            print(f"QR Code data: {my_data}")
            if "http" in my_data:
                import webbrowser
                webbrowser.open(my_data)
                return

        cv2.imshow('QR Code Scanner', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


qr_code_scanner()
