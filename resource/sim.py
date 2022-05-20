import easyocr
import pytesseract

from flask import jsonify
from resource.ocrapp import similar, get_count_digits


def sim_app(path):
    img = path
    reader = easyocr.Reader(['id'], gpu=False)
    result = reader.readtext(path, detail=1)

    sim_text = ''
    no_text = ''
    nama_text = ''
    ttl_text = ''
    jk_text = ''
    gd_text = ''
    alamat_text = ''
    pekerjaan_text = ''
    provinsi_text = ''
    masa_berlaku_text = ''

    for key, value in enumerate(result):

        text = value[1]

        # print(text)

        if similar("SURAT IZIN MENGEMUDI", text) > 0.7:
            sim_text = result[key + 1][1].replace("-", "")  # get SIM TYPE

            if sim_text.isnumeric():
                crop_img_sim = img[
                    result[key + 1][0][0][1] - 27: result[key + 1][0][2][1] - 25,
                    result[key + 1][0][0][0] + 30: result[key + 1][0][2][0] - 30
                ]

                sim_text_idx = pytesseract.image_to_string(
                    crop_img_sim, config='--psm 10 --oem 3')

                # get SIM TYPE
                if 'C' in sim_text_idx:
                    sim_text = 'C'
                if 'B' in sim_text_idx:
                    sim_text = 'B'
                if 'A' in sim_text_idx:
                    sim_text = 'A'

        if result[key][1].replace("-", "").isnumeric():
            if get_count_digits(int(result[key][1].replace("-", ""))) > 9:
                no_text = result[key][1]  # get NIK
                nama_text = result[key + 1][1]  # get Nama
                ttl_text = result[key + 2][1]  # get TTL
                jk_text = result[key + 3][1].split("-")[1]

                gd_text_idx = result[key + 3][1].split("-")[0]
                if 'O' in gd_text_idx:
                    gd_text = 'O'
                if 'o' in gd_text_idx:
                    gd_text = 'O'
                if '0' in gd_text_idx:
                    gd_text = 'O'
                if 'AB' in gd_text_idx:
                    gd_text = 'AB'
                if 'B' in gd_text_idx:
                    gd_text = 'B'
                if 'A' in gd_text_idx:
                    gd_text = 'A'

                alamat_text = result[key + 4][1] + ' ' + \
                    result[key + 5][1] + ' ' + result[key + 6][1]
                pekerjaan_text = result[key + 7][1]
                provinsi_text = result[key + 8][1]
                masa_berlaku_text = result[key + 9][1]

    # print('SIM : ' + sim_text)
    # print('NIK : ' + no_text)
    # print('Nama : ' + nama_text)
    # print('TTL : ' + ttl_text)
    # print('JK : ' + jk_text)
    # print('GD : ' + gd_text)
    # print('Alamat : ' + alamat_text)
    # print('Pekerjaan : ' + pekerjaan_text)
    # print('Provinsi : ' + provinsi_text)
    # print('Masa Berlaku : ' + masa_berlaku_text)

    return jsonify({
        "card_type": "SIM",
        "data": {
            'sim_type': sim_text,
            'provinsi': provinsi_text,
            'no': no_text,
            'nama': nama_text,
            'ttl': ttl_text,
            'jk': jk_text,
            'gd': gd_text,
            'alamat': alamat_text,
            'pekerjaan': pekerjaan_text,
            'provinsi': provinsi_text,
            'berlaku': masa_berlaku_text
        }
    })


# sim_app('upload/sim-002.jpg')
