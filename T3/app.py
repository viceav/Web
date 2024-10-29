import datetime
import hashlib
import os
import uuid

import filetype
from flask import Flask, jsonify, render_template, request, send_file, url_for
from PIL import Image
from werkzeug.utils import secure_filename

from db import db
from utils.validations import validate, validateComment

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.secret_key = 'super_secret_1234567890'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1000 * 1000  # 1 megabyte
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def timeNow():
    return datetime.datetime.now().isoformat(' ', "seconds")


def saveImg(img):
    _filename = hashlib.sha256(
        secure_filename(img.filename)  # nombre del archivo
        .encode("utf-8")  # encodear a bytes
    ).hexdigest()
    _extension = filetype.guess(img).extension
    img_filename = f"{_filename}_{str(uuid.uuid4())}.{_extension}"

    # 2. save img as a file
    # Save the original file
    path = os.path.join(app.config["UPLOAD_FOLDER"], img_filename)
    img.save(path)

    # Save each different size for the front end
    with Image.open(f"{path}") as im:
        im.resize((120, 120)).save(
            os.path.join(app.config['UPLOAD_FOLDER'], "120", img_filename))
        im.resize((640, 480)).save(
            os.path.join(app.config['UPLOAD_FOLDER'], "640", img_filename))
        im.resize((1280, 1024)).save(
            os.path.join(app.config['UPLOAD_FOLDER'], "1280", img_filename))

    return path, img_filename


@app.route("/")
def index():
    return send_file('static/html/index.html')


@app.route("/agregar-donacion", methods=["GET", "POST"])
def donacion():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        number = request.form['number']
        regiones = request.form['Regiones']
        comuna = request.form['Comunas']
        device = request.form.getlist('device')
        description = request.form.getlist('description')
        deviceType = request.form.getlist('type')
        uso = request.form.getlist('use')
        state = request.form.getlist('state')
        isValid = validate(username, email, number, regiones, comuna, device,
                           deviceType, uso, state, request.files)
        if not isValid:
            return render_template("agregar-donacion.html", error=not isValid)
        else:
            # save confession in db
            fecha_creacion = timeNow()
            db.insertContact(username, email, number, comuna, fecha_creacion)
            thisContactId = db.getContactId(username, email, number, comuna,
                                            fecha_creacion)

            for i in range(len(device)):
                db.insertDispositivo(thisContactId, device[i], description[i],
                                     deviceType[i], uso[i], state[i])

            for i in range(len(device)):
                if i == 0:
                    for image in request.files.getlist('images'):
                        path, filename = saveImg(image)
                        thisDevice = db.getDispositivoId(
                            thisContactId, device[i], description[i],
                            deviceType[i], uso[i], state[i])
                        db.insertArchivo(path, filename, thisDevice)

                else:
                    for image in request.files.getlist(f'images-{i+1}'):
                        path, filename = saveImg(image)
                        thisDevice = db.getDispositivoId(
                            thisContactId, device[i], description[i],
                            deviceType[i], uso[i], state[i])
                        db.insertArchivo(path, filename, thisDevice)

            return render_template("agregar-donacion.html", success=True)
    else:
        return render_template("agregar-donacion.html")


@app.route("/ver-dispositivos/<int:offset>", methods=['GET'])
@app.route("/ver-dispositivos", methods=['GET'])
def verDispositivos(offset=None):
    if not offset:
        offset = 0
    data = []
    # Entregamos los dispositivos y r que indica si
    # existen o no más elementos que mostrar
    (devices, r) = db.ver5Dispositivos(offset * 5)
    for dispositivo in devices:
        tipo, nombre, estado, nombre_com, dispositivo_id, contacto_id = dispositivo
        archivos = []
        for img in db.getArchivoById(dispositivo_id):
            img_route = f"uploads/120/{img[0]}"
            archivos.append(
                {"path_image": url_for('static', filename=img_route)})
        data.append({
            "tipo": tipo,
            "nombre": nombre,
            "estado": estado,
            "nombre_com": nombre_com,
            "fotos": archivos,
            "contacto_id": contacto_id,
            "dispositivo_id": dispositivo_id,
        })
    return render_template("ver-dispositivos.html",
                           data=(data, r),
                           offset=offset)


@app.route("/informacion-dispositivos", methods=["GET", 'POST'])
def infoDispositivo():
    dispositivo_id = request.args.get('dis_id')
    contacto_id = request.args.get('co_id')
    dis_nombre, dis_descripcion, dis_tipo, dis_anos_uso, dis_estado = db.getDispositivoInfo(
        dispositivo_id)
    co_nombre, co_email, co_celular, co_comuna_id = db.getContactInfo(
        contacto_id)

    com_nombre, region_id = db.getComunaInfo(co_comuna_id)

    archivos = []
    index = 0
    for img in db.getArchivoById(dispositivo_id):
        img_route = f"uploads/640/{img[0]}"
        img_route_full = f"uploads/1280/{img[0]}"
        archivos.append({
            "path_image":
            url_for('static', filename=img_route),
            "path_image_full":
            url_for('static', filename=img_route_full),
            "index":
            index
        })
        index += 1

    dispositivo = {
        "nombre": dis_nombre,
        "descripcion": dis_descripcion,
        "tipo": dis_tipo,
        "uso": dis_anos_uso,
        "estado": dis_estado,
        "fotos": archivos
    }

    contacto = {
        "nombre": co_nombre,
        "email": co_email,
        "celular": co_celular,
        "comuna": com_nombre,
        "region": db.getRegionName(region_id)
    }

    comments = []
    for comment in db.getComments(dispositivo_id):
        name, text, date = comment
        comments.append({"name": name, "text": text, "date": date})

    if request.method == 'POST':
        name = request.form['name']
        text = request.form['text']

        isValid = validateComment(name, text)

        if not isValid:
            return render_template('informacion-dispositivo.html',
                                   dis=dispositivo,
                                   co=contacto,
                                   comments=comments,
                                   error=True)
        else:
            date = timeNow()
            db.insertComment(name, text, date, dispositivo_id)
            comments.insert(0, {"name": name, "text": text, "date": date})

    return render_template(
        'informacion-dispositivo.html',
        dis=dispositivo,
        co=contacto,
        comments=comments,
    )


@app.route("/static/region-comuna.json", methods=["GET"])
def regionJson():
    return send_file('static/region-comuna.json')


@app.route('/tipo-dispositivos', methods=["GET"])
def tipoDispositivos():
    data = []
    for tipoDispotivo in db.getTipoDispositivo():
        tipo, count = tipoDispotivo
        data.append({"name": tipo, "y": count})

    return jsonify(data)


@app.route('/contactos-por-comuna', methods=["GET"])
def contactosPorComuna():
    data = []
    for contactosPorComuna in db.getContactosComuna():
        comuna, count = contactosPorComuna
        data.append({"name": comuna, "y": count})

    return jsonify(data)


@app.route('/grafico/tipo-dispositivos', methods=["GET"])
def graficoTipoDispositivos():
    return send_file('static/html/dispositivos.html')


@app.route('/grafico/contactos-comuna', methods=["GET"])
def graficoContactosComuna():
    return send_file('static/html/comunas.html')


if __name__ == "__main__":
    app.run(debug=True)
