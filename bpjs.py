import cv2
import easyocr
import pytesseract

from flask import jsonify
from ocrapp import detect, similar


def bpjs_app(path):
    img = cv2.imread(path)
    reader = easyocr.Reader(['id'], gpu=False)
    result = reader.readtext(path, detail=1)

    no_text = ''
    nik_text = ''
    nama_text = ''
    ttl_text = ''
    alamat_text = ''
    faskes_text = ''

    for key, value in enumerate(result):

        text = value[1]

        # print(text)

        if similar("Nomor Kartu", text) > 0.7:
            no_text = result[key + 1][1]

        if similar("Nama", text) > 0.7:
            nama_text = result[key + 1][1]

        if similar("Alamat", text) > 0.7:
            crop_img_alamat = img[
                value[0][0][1] - 5: value[0][2][1] + 35,
                value[0][0][0]: value[0][2][0] + 700
            ]

            alamat_text_idx = reader.readtext(crop_img_alamat, detail=1)

            for key_alamat, value_alamat in enumerate(alamat_text_idx):
                if similar("Alamat", value_alamat[1]) < 0.7:
                    alamat_text += str(alamat_text_idx[key_alamat][1])

        if similar("Tanggal Lahir", text) > 0.7 or similar("Tanggal", text) > 0.7:
            crop_img_ttl = img[
                value[0][0][1] - 10: value[0][2][1],
                value[0][0][0]: value[0][2][0] + 265
            ]

            ttl_text_idx = reader.readtext(crop_img_ttl, detail=1)

            for key_ttl, value_ttl in enumerate(ttl_text_idx):

                if similar("Tanggal Lahir", value_ttl[1]) > 0.7 or similar("Tanggal", value_ttl[1]) > 0.7:
                    ttl_text = ttl_text_idx[key_ttl + 1][1]
                    ttl_text_list = list(ttl_text)
                    if ttl_text_list[0] == '7':
                        ttl_text_list[0] = '1'

                    ttl_text = ''.join(ttl_text_list)

        if similar("NIK", text) > 0.8:
            nik_text = result[key + 1][1]

        if similar("Faskes Tingkat 1", text) > 0.7 or similar("Faskes", text) > 0.7:
            faskes_text = result[key + 1][1]

    # print('No : ' + no_text)
    # print('NIK : ' + nik_text)
    # print('Nama : ' + nama_text)
    # print('TTL : ' + ttl_text)
    # print('Alamat : ' + alamat_text)
    # print('Faskes : ' + faskes_text)

    return jsonify({
        "card_type": "BPJS",
        "data": {
            'no': no_text,
            'nik': nik_text,
            'nama': nama_text,
            'ttl': ttl_text,
            'nalamat': alamat_text,
            'faskes': faskes_text,
        }
    })


# bpjs_app('upload/bpjs-001.jpg')
