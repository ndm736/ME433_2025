
# sudo apt-get install python3-pip
# python3 -m pip install pyserial
# sudo apt-get install python3-matplotlib


import matplotlib.pyplot as plt 

import serial
ser = serial.Serial('/dev/tty.usbmodem101')
print('Opening port: ')
print(ser.name)

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
reds = np.zeros((60, 80), dtype=np.uint8)
greens = np.zeros((60, 80), dtype=np.uint8)
blues = np.zeros((60, 80), dtype=np.uint8)

has_quit = False
# menu loop
while not has_quit:
    selection = input('\nENTER COMMAND: ')
    selection_endline = selection+'\n'
     
    # send the command 
    ser.write(selection_endline.encode()); # .encode() turns the string into a char array

    if (selection == 'c'):
        for t in range(4800):
            dat_str = ser.read_until(b'\n'); 
            i,r,g,b = list(map(int,dat_str.split())) 
            row = i//80
            col = i%80
            reds[row][col] = r
            greens[row][col] = g
            blues[row][col] = b
            print(i)
            #print(str(i)+" "+str(r)+ " "+ str(g) + " " +str(b))

        # Stack arrays to form an RGB image
        rgb_array = np.stack((reds, greens, blues), axis=-1)

        # Convert to an image using PIL
        image = Image.fromarray(rgb_array)

        # Display the image using Matplotlib
        plt.imshow(image)
        plt.axis("off")  # Hide axes
        plt.show()
    elif (selection == 'q'):
        print('Exiting client')
        has_quit = True; # exit client
        # be sure to close the port
        ser.close()
    else:
        print('Invalid Selection ' + selection_endline)
