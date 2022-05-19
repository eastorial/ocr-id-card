import os

from flask import Flask, jsonify, request

from detect_card import detect
from ktp import ktp_app
from sim import sim_app
from npwp import npwp_app
from bpjs import bpjs_app

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


@app.route("/ocr/ktp")
def ktp_index():
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

    return ktp_app(path)


@app.route("/ocr/sim")
def sim_index():
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

    return sim_app(path)


@app.route("/ocr/npwp")
def npwp_index():
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

    return npwp_app(path)
