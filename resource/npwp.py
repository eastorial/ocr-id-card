import easyocr
import cv2

from flask import jsonify
from resource.ocrapp import similar, get_count_digits


def npwp_app(reader, path):

    img = cv2.imread(path)
    result = reader.readtext(img, detail=1)

    no_text = ""
    nama_text = ""
    nik_text = ""
    alamat_text = ""
    kpp_text = ""

    for key, value in enumerate(result):

        text = value[1]

        if text.replace(".", "").replace("-", "").isnumeric():
            if get_count_digits(int(text.replace(".", "").replace("-", ""))) == 15:
                no_text = text  # get no

                crop_img_nama = img[
                    result[key][0][0][1]: result[key][0][2][1] + 20,
                    result[key][0][0][0] - 80: result[key][0][2][0]
                ]

                nama_text_idx = reader.readtext(crop_img_nama, detail=1)

                for nama_key, nama_value in enumerate(nama_text_idx):
                    nama_text = nama_value[1]  # get nama

            if get_count_digits(int(text.replace(".", "").replace("-", ""))) == 16:
                nik_text = text  # get nik

                crop_img_alamat = img[
                    result[key][0][0][1] + 25: result[key][0][2][1] + 70,
                    result[key][0][0][0] - 60: result[key][0][2][0] + 30
                ]

                alamat_text_idx = reader.readtext(
                    crop_img_alamat, detail=1, paragraph=True)

                for alamat_key, alamat_value in enumerate(alamat_text_idx):
                    alamat_text = alamat_value[1]  # get alamat

        if similar("KPP PRATAMA", text) > 0.45:
            kpp_text = text

    return jsonify({
        "card_type": "NPWP",
        "data": {
            'no': no_text,
            'nama':  nama_text,
            'nik': nik_text,
            'alamat': alamat_text,
            'kpp': kpp_text
        }
    })

#     print('no : ' + no_text)
#     print('nama :' + nama_text)
#     print('nik : ' + nik_text)
#     print('alamat : ' + alamat_text)
#     print('kpp : ' + kpp_text)


# ktp_app('upload/npwp-002.jpg')
