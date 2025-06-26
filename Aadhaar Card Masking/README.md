🆔 Aadhaar Card Masking with Python & OCR
A simple Python script that scans an image for an Indian Aadhaar number and automatically masks the first 8 digits for privacy. This is especially helpful when handling documents that need to be shared but should not expose personal identity information.

🧠 What It Does
This script:
1.) Reads an image that potentially contains an Aadhaar number.
2.) Uses OCR (Tesseract) to extract all text from the image.
3.) Searches for Aadhaar-style numbers in the format 1234 5678 9012.
4.) Detects and masks the first 8 digits (i.e., 12345678) with white boxes and black "X" overlays.
5.) Saves the final masked image for safe use or sharing.

⚙️ Requirements
-> Python 3.x
-> Tesseract OCR
-> OpenCV (cv2)
-> pytesseract

pip install opencv-python pytesseract
💡 Tesseract Path: Don’t forget to update the script with your installed Tesseract path:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

🚀 How to Use
Place the image file (e.g., before_masking.png) in the project folder.
1.) Run the script:
2.) python mask_aadhaar.py
3.) The processed output will be saved as after_masking.png.

🔍 How Aadhaar is Detected
The Aadhaar format is three blocks of 4-digit numbers (e.g., 1234 5678 9012). The script searches for three consecutive words that match \d{4} using OCR data and combines them.
Once found, it extracts the character-level positions of the first 8 digits and masks them individually with:
- A white rectangle to hide the original number.
- A centered black "X" for visibility and format indication.

🔐 Why Mask Aadhaar?
The Aadhaar number is a highly sensitive and unique identifier in India. Masking at least the first 8 digits helps reduce the risk of identity theft while still retaining a verifiable structure in case limited validation is needed.

🛠 Customization
- To mask all 12 digits, simply increase masked_count < 8 to masked_count < 12.
- You can also switch masking to blur, pixelation, or other styles by modifying the drawing logic.

🤝 Contributing
Want to improve it? Found an edge case? PRs are welcome!
