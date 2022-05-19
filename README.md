OCR for SIM, KTP, BPJS, and NPWP

how to run : <br>
create virtual environment

<ol>
   <li> python3 -m venv env
   <li> source env/bin/activate
</ol>
upgarde pip (optional)
<ol>
   <li> pip install --upgrade pip
</ol>
install package

<ol>
   <li> pip install -r requirements.txt
</ol>
   <br>
   or
   <br>
<ol>
   <li> pip install pillow
   <li> pip install flask
   <li> pip install opencv-python==4.5.4.60
   <li> pip install imutils
   <li> pip install pytesseract
   <li> pip install easyocr
</ol>
run

<ol>
   <li> FLASK_APP=app.py FLASK_ENV=development flask run
</ol>
