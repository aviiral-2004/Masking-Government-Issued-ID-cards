Masking-Government-Issued-ID-cards
🔒 PAN Card Masking with Python & OCR A Python script that automatically detects and masks the first 6 characters of an Indian PAN (Permanent Account Number) from an image using OCR (Optical Character Recognition). Useful for anonymizing PAN cards in documents before sharing them publicly.

🧠 What It Does This script: 1.) Loads an image containing a PAN card. 2.) Uses Tesseract OCR to extract text data. 3.) Detects the PAN number using regex (ABCDE1234F format). 4.) Locates and masks the first 6 characters of the PAN with white boxes and black X’s. 5.) Saves the anonymized image for safe sharing.

⚙️ Requirements 1.) Python 3.x 2.) Tesseract OCR (Make sure it's installed and the path is configured) 3.) OpenCV (cv2) 4.) pytesseract

Install dependencies using pip: -> pip install opencv-python pytesseract Make sure Tesseract is properly installed and added to your system PATH or update this line in the code: -> pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

🚀 How to Use Place your PAN card image in the same folder as the script (e.g., before_masking.png).

Run the script: -> python pancard_masking.py

Output image (after_masking.png) will be saved in the same directory.

🔍 How PAN is Detected The script searches for text matching this regex: -> [A-Z]{5}[0-9]{4}[A-Z] This corresponds to the standard format of Indian PAN numbers.

🔐 Why Only the First 6 Characters? The first 5 letters typically identify the cardholder type and name initials, which can be sensitive. Masking these allows the document to retain some validity (e.g., for format checks) while protecting identity.

🛠 Customization To mask the entire PAN instead of the first 6 characters, adjust the loop condition. You can change the masking style (e.g., use blur instead of white box with "X").

🤝 Contributing Pull requests are welcome! Feel free to fork and improve the project.
