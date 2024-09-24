from flask import Flask, render_template, request, send_file

from utils.validations import validate

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.secret_key = 'super_secret_1234567890'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1000 * 1000  # 1 megabyte
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
        deviceType = request.form.getlist('type')
        uso = request.form.getlist('use')
        state = request.form.getlist('state')
        isValid = validate(username, email, number, regiones, comuna, device,
                           deviceType, uso, state, request.files)
        if not isValid:
            return render_template("agregar-donacion.html", error=not isValid)
        else:
            return render_template("agregar-donacion.html", success=True)
    else:
        return render_template("agregar-donacion.html")


@app.route("/static/region-comuna.json", methods=["GET"])
def regionJson():
    return send_file('static/region-comuna.json')


if __name__ == "__main__":
    app.run(debug=True)
