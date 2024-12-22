import cv2
import numpy as np
import imutils

# Slope of line function
def Slope(a, b, c, d):
    return (d - b) / (c - a)

# Reading Image
beltframe = cv2.imread(r"C:\Users\HP\Desktop\bai\bai.png")

# Check if the image is loaded successfully
if beltframe is None:
    print("Error: Image not found!")
    exit()

# Resizing The Image
beltframe = imutils.resize(beltframe, height=800)

# Converting To GrayScale
beltgray = cv2.cvtColor(beltframe, cv2.COLOR_BGR2GRAY)

# No Belt Detected Yet
belt = False

# Blurring The Image For Smoothness (increased kernel size)
blur = cv2.blur(beltgray, (3, 3))

# Converting Image To Edges
edges = cv2.Canny(blur, 50, 400)

# Previous Line Slope
ps = 0

# Previous Line Co-ordinates
px1, py1, px2, py2 = 0, 0, 0, 0

# Extracting Lines using Hough Line Transform
lines = cv2.HoughLinesP(edges, 1, np.pi / 270, 30, maxLineGap=20, minLineLength=170)

# If "lines" Is Not Empty
if lines is not None:
    # Loop through lines
    for line in lines:
        # Co-ordinates Of Current Line
        x1, y1, x2, y2 = line[0]

        # Slope Of Current Line
        s = Slope(x1, y1, x2, y2)

        # If Current Line's Slope Is Between 0.7 and 2
        if (abs(s) > 0.7) and (abs(s) < 2):

            # If Previous Line's Slope Is Within the Same Range
            if (abs(ps) > 0.7) and (abs(ps) < 2):

                # If Both Lines Are Not Too Far From Each Other
                if ((abs(x1 - px1) > 5) and (abs(x2 - px2) > 5)) or ((abs(y1 - py1) > 5) and (abs(y2 - py2) > 5)):

                    # Plot the lines on the beltframe
                    cv2.line(beltframe, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    cv2.line(beltframe, (px1, py1), (px2, py2), (0, 0, 255), 3)

                    # Belt is detected
                    print("Belt Detected")
                    belt = True

        # Update previous slope and coordinates
        ps = s
        px1, py1, px2, py2 = line[0]

# If no belt is detected
if not belt:
    print("No Seatbelt Detected")

# Show the output image with detected lines
cv2.imshow("Seat Belt", beltframe)

# Wait until a key is pressed and close the window
cv2.waitKey(0)
cv2.destroyAllWindows()

