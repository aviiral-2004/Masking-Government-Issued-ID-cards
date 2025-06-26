#🛡️ Identity Masking Toolkit (PAN | Aadhaar | Voter ID)
A Python-based toolkit for automatically detecting and masking sensitive information in Indian identity documents like PAN Cards, Aadhaar Cards, and Voter ID Cards using OCR (Tesseract) and OpenCV.
Whether you're building a secure document processing pipeline, anonymizing IDs for research datasets, or handling personal information with care—this project helps you protect privacy while maintaining document structure.

🔧 Setup Instructions
Install Python packages:
pip install opencv-python pytesseract
Install Tesseract OCR:
Download from tesseract-ocr.github.io
Update the tesseract_cmd path in each script:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

✅ Supported Formats
ID Type	Pattern Example	Masking Type
PAN Card	ABCDE1234F	First 6 characters masked
Aadhaar Card	1234 5678 9012	First 8 digits masked
Voter ID Card	ABC1234567	Entire ID masked
All formats are detected using regex + OCR and masked using OpenCV drawing methods.

🚀 How to Use
Go into the respective folder and run the script:
python mask_pan.py
Change the image name in the script or replace before_masking.png with your own input file.

📁 Sample Input & Output
Each script saves:
-> Input image: before_masking.png
-> Output (masked) image: after_masking.png


🔐 Why This Matters
With rising concerns around data privacy, masking personal identifiers is crucial. This project enables:
1.) Privacy-safe document sharing
2.) Secure KYC data handling
3.) Anonymized datasets for research or analytics

🤝 Contributions Welcome
Have a better regex? Want to add support for other ID types or use deep learning? Pull requests are welcome!
