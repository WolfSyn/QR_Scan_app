import tkinter as tk
from tkinter import messagebox
import cv2
from pyzbar.pyzbar import decode

# This program open's your local camera so it may start scanning the selected QR code you have on hand & will take you to website on that scanned QR.

# - note you need to have a camera connected so that the script won't run and will start to give error if it does not detect camera...

#V2 - when scanning QR code, it will track the URL on screen real time & will give link in output box...

#V3 - Added GUI support - next version will add the output in GUI instead of using the output in pycharm...

def start_scanning():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        for barcode in decode(frame):
            qr_data = barcode.data.decode('utf-8')
            print(f"QR Code Data: {qr_data}")

            #Draw a rectangle around the detected QR code
            points = barcode.polygon
            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points],dtype=np.float))
                points = hull.tolist()
            n = len(points)
            for j in range(n):
                cv2.line(frame, tuple(points[j]), tuple(points[(j+1)%n]), (255,0,0), 3)

            #Print the QR code data on the frame
            x, y, w, h = barcode.rect
            cv2.putText(frame, qr_data, (x, y -10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 225, 0), 2)

        cv2.imshow('QR Code Scanner', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

def on_start():
    messagebox.showinfo("Start", "Ready to scan QR codes!")
    start_scanning()

#Create the main window
root = tk.Tk()
root.title("QR Code Scanner")

#Create a button to start scanning
start_button = tk.Button(root, text="Start Scanning", command=on_start)
start_button.pack(pady=28)

#Run the GUI event loop
root.mainloop()
