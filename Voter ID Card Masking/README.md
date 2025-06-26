🗳️ Voter ID Card Masking with Python & OCR
A Python script that automatically detects and masks Indian Voter ID card numbers from images using Optical Character Recognition (OCR). Perfect for anonymizing Voter ID details before sharing documents for verification or compliance.

🧠 What It Does
This script:
1.) Loads an image that contains a Voter ID card.
2.) Uses Tesseract OCR to extract text from the image.
3.) Searches for the EPIC number (Voter ID), which usually follows a format like ABC1234567.
4.) Masks the entire Voter ID number using white rectangles and black “X” characters.
5.) Saves the masked image for secure sharing.

⚙️ Requirements
Python 3.x
Tesseract OCR
OpenCV (cv2)
pytesseract
Install required packages with:

pip install opencv-python pytesseract
🛠 Note: Update this line in the code with your correct Tesseract installation path:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

🚀 How to Use
Save your Voter ID image as before_masking.png (or edit the script to point to a different file).
Run the script:
python mask_voter_id.py
The masked output will be saved as after_masking.png.

🔍 How Voter ID is Detected
The script uses a regex pattern to identify Indian Voter ID numbers, typically in the format:

[A-Z]{3}[0-9]{7}
Example: ABC1234567
After identifying the string, the script locates the individual characters using OCR’s bounding box data and places white blocks with "X" over each one.

🔐 Why Mask the Voter ID?
The EPIC number on Indian Voter ID cards is a personal and confidential identifier. Masking this number helps:
1.) Prevent misuse or identity fraud
2.) Ensure compliance with data protection regulations
3.) Share documents securely with third parties

🛠 Customization
To partially mask (e.g., only last 5 digits), change the masked_count logic.
Want to use blur instead of boxes? Replace the drawing logic with an OpenCV blur region.
Add multi-image batch processing for document sets.

🤝 Contributing
Feel free to fork the repo, improve detection accuracy, or add support for multilingual OCR. PRs and suggestions are always welcome.

