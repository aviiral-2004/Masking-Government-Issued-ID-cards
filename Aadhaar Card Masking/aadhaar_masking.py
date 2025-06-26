import cv2
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# image = cv2.imread("dataset_aadhar/img1.jpg")
image = cv2.imread("before_masking.png")
if image is None:
    print("Error: Image not found.")
    exit()

# Preprocess image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3, 3), 0)
thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 11, 2)

# Detect words (for finding Aadhaar format)
data = pytesseract.image_to_data(thresh, output_type=pytesseract.Output.DICT)
aadhaar_number = None
start_index = None

for i in range(len(data['text']) - 2):
    word1 = data['text'][i].strip()
    word2 = data['text'][i+1].strip()
    word3 = data['text'][i+2].strip()

    if re.fullmatch(r'\d{4}', word1) and re.fullmatch(r'\d{4}', word2) and re.fullmatch(r'\d{4}', word3):
        aadhaar_number = word1 + word2 + word3
        start_index = i
        break

if aadhaar_number:
    print(f"[SUCCESS] Aadhaar Found: {aadhaar_number}")

    # Character-wise bounding boxes
    h_img, w_img = image.shape[:2]
    boxes = pytesseract.image_to_boxes(thresh)

    masked_count = 0
    for b in boxes.splitlines():
        parts = b.split()
        if len(parts) == 6:
            ch, x1, y1, x2, y2, _ = parts
            if masked_count < 8 and ch.isdigit() and ch == aadhaar_number[masked_count]:
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                y1 = h_img - y1
                y2 = h_img - y2

                # Draw white rectangle over character
                cv2.rectangle(image, (x1, y2), (x2, y1), (255, 255, 255), -1)

                # Optional: Put 'X' in the center
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.6
                thickness = 1
                text_size = cv2.getTextSize("X", font, font_scale, thickness)[0]
                text_x = x1 + (x2 - x1 - text_size[0]) // 2
                text_y = y2 + (y1 - y2 + text_size[1]) // 2
                cv2.putText(image, "X", (text_x, text_y), font, font_scale, (0, 0, 0), thickness)

                masked_count += 1

    cv2.imwrite("after_masking.png", image)
    print("[INFO] Aadhaar masked with block-wise rectangles.")
    cv2.imshow("Masked Aadhaar", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print("[ERROR] Aadhaar number not detected.")
