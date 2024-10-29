import cv2
import tkinter as tk
from tkinter import Label, messagebox
from PIL import Image, ImageTk
import qrcode
from pyzbar.pyzbar import decode

# This program open's your local camera so it may start scanning the selected QR code you have on hand & will take you to website on that scanned QR.

# - note you need to have a camera connected so that the script won't run and will start to give error if it does not detect camera...

# V2 - when scanning QR code, it will track the URL on screen real time & will give link in output box...

# V3 - Added GUI support - next version will add the output in GUI instead of using the output in pycharm...

# V4  -- gives you an option to create your own QR by adding your desired URL link

# V5 -- added a stop button sto stop using camera --- Button not working keeps freezing the script
def start_camera():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        for barcode in decode(frame):
            qr_data = barcode.data.decode('utf-8')
            print(f"QR Code Data: {qr_data}")

            # Draw a rectangle around the detected QR code
            points = barcode.polygon
            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float))
                points = hull.tolist()
            n = len(points)
            for j in range(n):
                cv2.line(frame, tuple(points[j]), tuple(points[(j + 1) % n]), (255, 0, 0), 3)

            # Print the QR code data on the frame
            x, y, w, h = barcode.rect
            cv2.putText(frame, qr_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 225, 0), 2)

        cv2.imshow('QR Code Scanner', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def generate_qr():
    url = url_entry.get()
    if url:
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("output.png")
        img = Image.open("output.png")
        img = ImageTk.PhotoImage(img)
        qr_label.config(image=img)
        qr_label.image = img
        messagebox.showinfo("QR Code Generated", f"Here is your QR code: {url}")
    else:
        messagebox.showwarning("Error", "Please enter a URL.")

# Create the main window
root = tk.Tk()
root.title("QR Code Generator and Scanner")

# Create a label and entry for URL
url_label = tk.Label(root, text="Enter URL:")
url_label.pack()
url_entry = tk.Entry(root)
url_entry.pack()

# Create a button to generate QR code
generate_button = tk.Button(root, text="Generate QR Code", command=generate_qr)
generate_button.pack(pady=10)

# Create a button to start the camera
start_button = tk.Button(root, text="Start Camera", command=start_camera)
start_button.pack(pady=10)

# Create a button to Stop the Camera
stop_button = tk.Button(root, text="Stop Camera", command=lambda: cv2.destroyAllWindows())
stop_button.pack(pady=10)

# Create a label to display QR code
qr_label = Label(root)
qr_label.pack(pady=10)

# Run the application
root.mainloop()
