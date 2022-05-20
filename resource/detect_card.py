import easyocr
import cv2

from resource.ocrapp import similar


def detect(reader, path):
    img = cv2.imread(path)
    result = reader.readtext(img, detail=1)

    card_type = ''

    for key, value in enumerate(result):

        text = value[1]

        if similar("Berlaku Hingga", text) > 0.6:
            card_type = 'KTP'
            break

        if similar("DIREKTORAT JENDERAL PAJAK", text) > 0.7:
            card_type = 'NPWP'
            break

        if similar("SURAT IZIN MENGEMUDI", text) > 0.7:
            card_type = 'SIM'
            break

        if similar("Kartu Indonesia Sehat", text) > 0.7 or similar("Faskes", text) > 0.7:
            card_type = 'BPJS'
            break

    return card_type
