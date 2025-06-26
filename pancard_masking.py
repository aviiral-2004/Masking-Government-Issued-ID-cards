import cv2
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image_path = "before_masking.png" # enter the image name instead of this
image = cv2.imread(image_path)
if image is None:
    print("[ERROR] Image not found.")
    exit()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
filtered = cv2.bilateralFilter(gray, 11, 17, 17)
_, thresh = cv2.threshold(filtered, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# First, find the PAN number using word-level detection
config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
data = pytesseract.image_to_data(thresh, output_type=pytesseract.Output.DICT, config=config)

pan_regex = r'\b[A-Z]{5}[0-9]{4}[A-Z]\b'
pan_number = None
pan_box = None

for i in range(len(data['text'])):
    word = data['text'][i].strip()
    if re.fullmatch(pan_regex, word):
        pan_number = word
        pan_box = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        break

if pan_number:
    print("[SUCCESS] PAN Detected:", pan_number)

    # Get per-character boxes
    h_img, w_img, _ = image.shape
    boxes = pytesseract.image_to_boxes(thresh, config=config)

    masked_count = 0
    for b in boxes.splitlines():
        ch, x1, y1, x2, y2, _ = b.split()

        if pan_number.startswith(ch, masked_count):
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            y1 = h_img - y1
            y2 = h_img - y2

            # Draw white rectangle
            cv2.rectangle(image, (x1, y2), (x2, y1), (255, 255, 255), -1)

            # Put 'X' in black, centered inside the rectangle
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.7
            thickness = 2
            text_size = cv2.getTextSize("X", font, font_scale, thickness)[0]

            text_x = x1 + (x2 - x1 - text_size[0]) // 2
            text_y = y2 + (y1 - y2 + text_size[1]) // 2

            cv2.putText(image, "X", (text_x, text_y), font, font_scale, (0, 0, 0), thickness)

            masked_count += 1
            if masked_count == 6:
                break

    output_path = "after_masking.png" # Output Image after masking
    cv2.imwrite(output_path, image)
    print(f"[INFO] Precisely masked first 6 characters. Output saved to '{output_path}'.")

else:
    print("[ERROR] PAN number not detected.")
