import cv2
import os
import math

# Haar cascade classifiers
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")


def process_passport_photos(input_path, output_path, width, height, max_kb, face_only=True):
    """
    Process passport size photos from input image and save cropped/resized ones.

    Args:
        input_path (str): Path of the input image.
        output_path (str): Folder to save processed images.
        width (int): Width of output photo in pixels.
        height (int): Height of output photo in pixels.
        max_kb (int): Max file size in KB.
        face_only (bool): If True, crop only the face. If False, include face + shoulders.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Read input image
    image = cv2.imread(input_path)
    if image is None:
        raise ValueError("Input image not found or not readable.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.2, 5)

    count = 0
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]

        # --- Detect eyes for alignment ---
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) >= 2:
            # Select two largest eyes
            eyes = sorted(eyes, key=lambda ex: ex[2] * ex[3], reverse=True)[:2]
            eyes = sorted(eyes, key=lambda ex: ex[0])  # sort left-right

            (ex1, ey1, ew1, eh1) = eyes[0]
            (ex2, ey2, ew2, eh2) = eyes[1]

            # Absolute eye centers
            eye_center1 = (x + ex1 + ew1 // 2, y + ey1 + eh1 // 2)
            eye_center2 = (x + ex2 + ew2 // 2, y + ey2 + eh2 // 2)

            dx = float(eye_center2[0] - eye_center1[0])
            dy = float(eye_center2[1] - eye_center1[1])
            angle = math.degrees(math.atan2(dy, dx))

            # Make sure center is float
            eyes_center = (
                float((eye_center1[0] + eye_center2[0]) / 2.0),
                float((eye_center1[1] + eye_center2[1]) / 2.0)
            )

            # Rotate whole image to align eyes horizontally
            M = cv2.getRotationMatrix2D(eyes_center, angle, 1.0)
            image = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Redetect face on rotated image
            faces_rotated = face_cascade.detectMultiScale(gray, 1.2, 5)
            if len(faces_rotated) > 0:
                (x, y, w, h) = faces_rotated[0]

        # --- Adjust crop region ---
        if face_only:
            crop_img = image[y:y+h, x:x+w]
        else:
            y1 = max(0, y - int(0.3 * h))       # space above head
            y2 = min(image.shape[0], y + int(1.5 * h))  # more space below chin
            x1 = max(0, x - int(0.2 * w))
            x2 = min(image.shape[1], x + int(1.2 * w))
            crop_img = image[y1:y2, x1:x2]

        # Resize
        resized = cv2.resize(crop_img, (width, height))

        # --- Compression loop ---
        quality = 95
        save_path = os.path.join(output_path, f"photo_{count+1}.jpg")

        while True:
            cv2.imwrite(save_path, resized, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
            if os.path.getsize(save_path) <= max_kb * 1024 or quality <= 20:
                break
            quality -= 5

        count += 1

    return count

