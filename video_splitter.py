import cv2

# read names of input video files
file = open("/Users/AdelynnMeow/Downloads/Robotics/video_names.txt", "r")
full_list = file.read()
names = full_list.split()

# loop through the videos
for name in names: 
    # create an object of class VideoCapture
    input_name = '/Users/AdelynnMeow/Downloads/Robotics/Videos/' + name + '.avi'
    capture = cv2.VideoCapture(input_name)

    # number of the current frames we are processing
    frame_number = 0

    # process frames
    while(True):
        # read frame
        success, frame = capture.read()
    
        if success:
            # convert the frame to grayscale
            grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            output_name = '/Users/AdelynnMeow/Downloads/Robotics/Output/' + name + '/' + name + '_' + str(frame_number) + '.jpg'
            # write the frame
            cv2.imwrite(output_name, grayscale)
        else:
            break

        frame_number += 1

    capture.release()