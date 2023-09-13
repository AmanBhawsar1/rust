import streamlit as st
from PIL import Image
import cv2
import numpy as np

def main():
    st.title('Image Processing using Streamlit')

    selected_box = st.sidebar.selectbox(
        'Choose one of the following',
        ('Welcome', 'Image Processing', 'Video', 'Face Detection', 'Feature Detection', 'Object Detection')
    )

    if selected_box == 'Welcome':
        welcome()
    elif selected_box == 'Image Processing':
        uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.image(image, use_column_width=True)
            process_option = st.radio("Select image processing option:", ('Thresholding', 'Contours', 'Erosion',
                                                                        'Dilation', 'Gaussian Blur', 'Sobel Edge Detection',
                                                                        'Canny Edge Detection', 'Median Filter', 'Hough Transform', 'Hough Circles'))
            if process_option == 'Thresholding':
                photo_threshold(image)
            elif process_option == 'Contours':
                photo_contours(image)
            elif process_option == 'Erosion':
                erosion(image)
            elif process_option == 'Dilation':
                dilation(image)
            elif process_option == 'Gaussian Blur':
                gaussian_blur(image)
            elif process_option == 'Sobel Edge Detection':
                sobel_edge(image)
            elif process_option == 'Canny Edge Detection':
                canny_edge(image)
            elif process_option == 'Median Filter':
                median_filter(image)
            elif process_option == 'Hough Transform':
                hough_transform(image)
            elif process_option == 'Hough Circles':
                hough_circles(image)
    elif selected_box == 'Video':
        video()
    elif selected_box == 'Face Detection':
        uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.image(image, use_column_width=True)
            face_detection(image)
    elif selected_box == 'Feature Detection':
        feature_detection()
    elif selected_box == 'Object Detection':
        uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.image(image, use_column_width=True)
            object_detection(image)

def welcome():
    st.subheader('A simple app that shows different image processing algorithms. You can choose the options'
                 + ' from the left. I have implemented only a few to show how it works on Streamlit. ' +
                 'You are free to add stuff to this app.')

def photo_threshold(image):
    st.header("Thresholding")

    x = st.slider('Change Threshold value', min_value=50, max_value=255)
    image_cv = np.array(image)
    image_gray = cv2.cvtColor(image_cv, cv2.COLOR_RGB2GRAY)
    ret, thresh1 = cv2.threshold(image_gray, x, 255, cv2.THRESH_BINARY)
    thresh1 = thresh1.astype(np.float64)
    st.image(thresh1, use_column_width=True, clamp=True)

def photo_contours(image):
    st.header("Contours")

    y = st.slider('Change Value to increase or decrease contours', min_value=50, max_value=255)

    if st.button('Detect Contours'):
        image_cv = np.array(image)
        imgray = cv2.cvtColor(image_cv, cv2.COLOR_RGB2GRAY)
        ret, thresh = cv2.threshold(imgray, y, 255, 0)
        image_contours, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        img = cv2.drawContours(image_cv.copy(), contours, -1, (0, 255, 0), 3)

        st.image(thresh, use_column_width=True, clamp=True)
        st.image(img, use_column_width=True, clamp=True)

def erosion(image):
    st.header("Erosion")
    kernel = np.ones((5, 5), np.uint8)
    image_cv = np.array(image)
    image_erosion = cv2.erode(image_cv, kernel, iterations=1)
    st.image(image_erosion, use_column_width=True, clamp=True)

def dilation(image):
    st.header("Dilation")
    kernel = np.ones((5, 5), np.uint8)
    image_cv = np.array(image)
    image_dilation = cv2.dilate(image_cv, kernel, iterations=1)
    st.image(image_dilation, use_column_width=True, clamp=True)

def gaussian_blur(image):
    st.header("Gaussian Blur")
    image_cv = np.array(image)
    image_blur = cv2.GaussianBlur(image_cv, (5, 5), 0)
    st.image(image_blur, use_column_width=True, clamp=True)

def sobel_edge(image):
    st.header("Sobel Edge Detection")
    image_cv = np.array(image)
    image_gray = cv2.cvtColor(image_cv, cv2.COLOR_RGB2GRAY)
    sobel_x = cv2.Sobel(image_gray, cv2.CV_64F, 1, 0, ksize=5)
    st.image(sobel_x, use_column_width=True, clamp=True)

def canny_edge(image):
    st.header("Canny Edge Detection")
    image_cv = np.array(image)
    image_gray = cv2.cvtColor(image_cv, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(image_gray, 50, 150)
    st.image(edges, use_column_width=True, clamp=True)

def median_filter(image):
    st.header("Median Filter")
    image_cv = np.array(image)
    image_blur = cv2.medianBlur(image_cv, 5)
    st.image(image_blur, use_column_width=True, clamp=True)

def hough_transform(image):
    st.header("Hough Transform")
    image_cv = np.array(image)
    image_gray = cv2.cvtColor(image_cv, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(image_gray, 50, 150)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
    if lines is not None:
        for rho, theta in lines[:, 0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(image_cv, (x1, y1), (x2, y2), (0, 0, 255), 2)
    st.image(image_cv, use_column_width=True, clamp=True)

def hough_circles(image):
    st.header("Hough Circles Detection")
    image_cv = np.array(image)
    image_gray = cv2.cvtColor(image_cv, cv2.COLOR_RGB2GRAY)
    circles = cv2.HoughCircles(image_gray, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=0, maxRadius=0)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            center = (circle[0], circle[1])
            radius = circle[2]
            cv2.circle(image_cv, center, radius, (0, 255, 0), 2)
    st.image(image_cv, use_column_width=True, clamp=True)

def face_detection(image):
    st.header("Face Detection using haarcascade")

    image_cv = np.array(image)
    image_gray = cv2.cvtColor(image_cv, cv2.COLOR_RGB2GRAY)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    st.text(f"{len(faces)} faces detected in the image.")

    for (x, y, w, h) in faces:
        cv2.rectangle(image_cv, (x, y), (x + w, y + h), (0, 255, 0), 2)

    st.image(image_cv, use_column_width=True, clamp=True)

def feature_detection():
    st.header("Feature Detection")
    # Add your feature detection code here

def object_detection(image):
    st.header("Object Detection")
    st.subheader("Please upload a haarcascade XML file for object detection.")
    
    uploaded_cascade = st.file_uploader("Upload a haarcascade XML file", type=["xml"])
    
    if uploaded_cascade is not None:
        cascade = cv2.CascadeClassifier(cv2.data.haarcascades + uploaded_cascade.name)

        if st.button('Detect Objects'):
            image_cv = np.array(image)
            image_gray = cv2.cvtColor(image_cv, cv2.COLOR_RGB2GRAY)

            objects = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            st.text(f"{len(objects)} objects detected in the image.")

            for (x, y, w, h) in objects:
                cv2.rectangle(image_cv, (x, y), (x + w, y + h), (0, 255, 0), 2)

            st.image(image_cv, use_column_width=True, clamp=True)

if __name__ == "__main__":
    main()

