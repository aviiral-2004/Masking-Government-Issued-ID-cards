import cv2
import pytesseract
import re

# Tesseract setup
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load image
image_path = "before_masked.png"
print("[INFO] Loading image:", image_path)
image = cv2.imread(image_path)
if image is None:
    print("[ERROR] Image not found.")
    exit()

print("[INFO] Image loaded successfully.")
print("[INFO] Preprocessing image...")

# Preprocessing
image = cv2.resize(image, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
denoised = cv2.fastNlMeansDenoising(gray, h=30)
thresh = cv2.adaptiveThreshold(denoised, 255,
                               cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 21, 15)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

print("[INFO] Preprocessing completed.")
print("[INFO] Running OCR...")

# OCR
custom_config = r'--oem 3 --psm 6'
data = pytesseract.image_to_data(morphed, output_type=pytesseract.Output.DICT, config=custom_config)

print("[INFO] OCR completed.")
words = [w for w in data['text'] if w.strip() != ""]
print(f"[DEBUG] Total non-empty words detected: {len(words)}")
print("[SAMPLE] First few detected words:", words[:10])

print("[INFO] Searching for ID number using regex...")
id_regex = r'\b[A-Z,0-9]{6}[0-9]{4}\b'
voter_id_number = None
voter_box = None

for i in range(len(data['text'])):
    clean_word = data['text'][i].strip()
    if re.fullmatch(id_regex, clean_word):
        voter_id_number = clean_word
        voter_box = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        break
config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

if voter_id_number:
    print("[SUCCESS] Voter ID Detected:", voter_id_number)

    h_img, w_img, _ = image.shape
    boxes = pytesseract.image_to_boxes(thresh, config=config)

    masked_count = 0
    for b in boxes.splitlines():
        ch, x1, y1, x2, y2, _ = b.split()
        if voter_id_number.startswith(ch, masked_count):
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

    cv2.imwrite('after_masked.png', image)
    cv2.imshow('output_image', image)
    print(f"[INFO] Precisely masked first 6 characters. Output saved to.")

else:
    print("[ERROR] ID number not detected using regex pattern.")
    print("[SUGGESTION] Check if ID format is different. Try changing regex to match the actual pattern.")
    print("[INFO] Full detected words:", words)
