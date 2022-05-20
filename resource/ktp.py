import re
import easyocr
import pytesseract

from flask import jsonify
from resource.ocrapp import detect, similar


def ktp_app(reader, path):

    img = detect(path)
    result = reader.readtext(img, detail=1)

    provinsi_text = ''
    kota_text = ''
    nik_text = ''
    nama_text = ''
    ttl_text = ''
    jk_text = ''
    gd_text = ''
    alamat_text = ''
    rtrw_text = ''
    kel_text = ''
    agama_text = ''
    kec_text = ''
    status_text = ''
    pekerjaan_text = ''
    kw_text = ''

    for key, value in enumerate(result):

        text = value[1]

        if similar("PROVINSI", text.split(' ')[0]) > 0.7:
            provinsi_text = text

        if similar("KOTA", text.split(' ')[0]) > 0.7 or similar("KABUPATEN", text.split(' ')[0]) > 0.7:
            kota_text = text

        if similar("NIK", text) > 0.7:
            nik_text_val = result[key + 1][1]

            if nik_text_val.isnumeric():
                nik_text = nik_text_val

        if similar("Nama", text) > 0.7:
            nama_text = result[key + 1][1]

        if similar("Tempat/Tgl lahir", text) > 0.7:
            if re.search(r'\d', result[key + 1][1]):
                ttl_text = result[key + 1][1]
            else:
                ttl_text = result[key + 1][1] + ' ' + result[key + 2][1]

            if '?' in ttl_text:
                ttl_text = ttl_text.replace('?', '2')

        if similar("Jenis Kelamin", text) > 0.7:
            jk_text = result[key + 1][1]

        if similar("Alamat", text) > 0.8:
            alamat_text = result[key + 1][1]

        if similar("RT/RW", text) > 0.7:
            rtrw_text = result[key + 1][1]

        if similar("Kel/Desa", text) > 0.7:
            kel_text = result[key + 1][1]

        if similar("Kecamatan", text) > 0.7:
            kec_text = result[key + 1][1]

        if similar("Agama", text) > 0.8:
            agama_text = result[key + 1][1]

        if similar("Status Perkawinan", text) > 0.7:
            status_text = result[key + 1][1]

        if similar("Pekerjaan", text) > 0.7:
            pekerjaan_text = result[key + 1][1]

        if similar("Kewarganegaraan", text) > 0.7:
            kw_text = result[key + 1][1]

        if similar("Gol", text) > 0.5 or similar("Gol. Darah", text) > 0.7:
            crop_img_gd = img[
                value[0][0][1]: value[0][2][1],
                value[0][0][0]: value[0][2][0] + 80
            ]

            gd_text_idx = pytesseract.image_to_string(crop_img_gd)
            gd_text_idx = gd_text_idx.split(' ')

            for key_gd, value_gd in enumerate(gd_text_idx):

                if similar("Gol", value_gd) > 0.5 or similar("Gol.Darah", value_gd) > 0.5 or similar("Darah", value_gd) > 0.5:
                    continue
                else:
                    try:

                        idx_gd = re.sub(
                            r'[^\w]', ' ', gd_text_idx[key_gd]).strip()

                        if 'O' in idx_gd:
                            gd_text = 'O'
                        if 'o' in idx_gd:
                            gd_text = 'O'
                        if '0' in idx_gd:
                            gd_text = 'O'
                        if 'AB' in idx_gd:
                            gd_text = 'AB'
                        if 'B' in idx_gd:
                            gd_text = 'B'
                        if 'A' in idx_gd:
                            gd_text = 'A'

                    except IndexError:
                        gd_text = '-'

        # print(text)

    return jsonify({
        "card_type": "KTP",
        "data": {
            'provinsi': provinsi_text,
            'kota': kota_text,
            'nik': nik_text,
            'nama': nama_text,
            'ttl': ttl_text,
            'jk': jk_text,
            'gd': gd_text,
            'alamat': alamat_text,
            'rt/rw': rtrw_text,
            'kel': kel_text,
            'agama': agama_text,
            'kec': kec_text,
            'status': status_text,
            'pekerjaan': pekerjaan_text,
            'kewarganegaraan': kw_text

        }
    })
    # print('Prov : ' + provinsi_text)
    # print('Kota :' + kota_text)
    # print('NIK : ' + nik_text)
    # print('Nama : ' + nama_text)
    # print('TTL : ' + ttl_text)
    # print('JK : ' + jk_text)
    # print('GD : ' + gd_text)
    # print('Alamat : ' + alamat_text)
    # print('RT/RW : ' + rtrw_text)
    # print('Kel : ' + kel_text)
    # print('Agama : ' + agama_text)
    # print('Kec : ' + kec_text)
    # print('Status : ' + status_text)
    # print('Pekerjaan : ' + pekerjaan_text)
    # print('Kewarganegaraan : ' + kw_text)


# ktp_app('upload/ktp-001.jpg')
