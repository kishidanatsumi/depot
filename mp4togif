import cv2
import imageio
import sys

input_file = sys.argv[1]
output_file = "output.gif"
fps = 60


def convert(input_file, output_file, fps=30):
    cap = cv2.VideoCapture(input_file)

    print("Input file:"+input_file)

    width = int(cap.get(3))
    height = int(cap.get(4))

    out = imageio.get_writer(output_file, fps=fps)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        out.append_data(frame)

    # Release resources
    cap.release()
    out.close()

    print("Output file:"+output_file)

convert(input_file, output_file, fps)
