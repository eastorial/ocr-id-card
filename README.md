OCR for SIM, KTP, BPJS, and NPWP

how to run : <br>
upgarde pip

<ol>
   <li> pip install --upgrade pip </li>
</ol>

install binary pyteseract

<ol>
   <li> sudo apt update </li>
   <li>sudo apt install tesseract-ocr </li>
   <li>sudo apt install libtesseract-dev </li>
</ol>

create virtual environment

<ol>
   <li> python3 -m venv env </li>
   <li> source env/bin/activate </li>
</ol>

install package

<ol>
   <li> pip install -r requirements.txt </li>
</ol>

or

<ol>
   <li> pip install pillow </li>
   <li> pip install flask </li>
   <li> pip install opencv-python==4.5.4.60 </li>
   <li> pip install imutils </li>
   <li> pip install pytesseract </li>
   <li> pip install easyocr </li>
</ol>

run

<ol>
   <li> FLASK_APP=app.py FLASK_ENV=development flask run </li>
</ol>
