import os

from flask import Flask, jsonify, request

from resource.detect_card import detect
from resource.ktp import ktp_app
from resource.sim import sim_app
from resource.npwp import npwp_app
from resource.bpjs import bpjs_app

UPLOAD_FOLDER = './upload'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/ocr")
def index():
    if 'file' not in request.files:
        return jsonify({
            "data": "no file"
        })

    file_upload = request.files['file']

    if file_upload.filename == '':
        return jsonify({
            "data": "file null"
        })

    path = os.path.join(app.config['UPLOAD_FOLDER'], file_upload.filename)
    file_upload.save(path)

    card_type = detect(path)

    if card_type == 'KTP':
        return ktp_app(path)
    if card_type == 'SIM':
        return sim_app(path)
    if card_type == 'NPWP':
        return npwp_app(path)
    if card_type == 'BPJS':
        return bpjs_app(path)
