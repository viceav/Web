import re

import filetype
from flask import flash


def validateName(name, index=-1):
    if not name:
        if index == -1:
            flash('Falta ingresar el Nombre del Donante')
        else:
            if index == 0:
                flash('Falta ingresar el Nombre del Dispositivo')
            else:
                flash(f'Falta ingresar el Nombre del Dispositivo {index+1}')
        return False
    lenghtValid = 80 >= len(name.strip()) >= 3
    if not lenghtValid:
        if index == -1:
            flash('Ingrese un Nombre de Donante válido')
        else:
            if index == 0:
                flash('Ingrese un Nombre válido para el Dispositivo')
            else:
                flash(
                    f'Ingrese un Nombre válido para el Dispositivo {index+1}')
    return lenghtValid


def validateEmail(email):
    if not email:
        flash('Falta ingresar el email')
        return False

    expr = r"^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$"
    isValid = re.match(expr, email)
    if not isValid:
        flash('Email incorrecto')
    return isValid


def validatePhoneNumber(phone):
    if phone != "":
        lenghtValid = len(phone) >= 8
        expr = r"^[0-9]+$"

        isValid = lenghtValid and re.match(expr, phone)
        if not isValid:
            flash('Número incorrecto')
        return isValid
    else:
        return True


def validateUso(uso, index):
    if not uso or not uso.isdigit():
        if index == 0:
            flash(
                'Ingrese un número válido para los Años de uso del Dispositivo'
            )
        else:
            flash(
                f'Ingrese un número válido para los Años de uso del Dispositivo {index+1}'
            )
        return False
    isValid = 99 >= int(uso.strip()) > 0
    if not isValid:
        if index == 0:
            flash(
                'Ingrese un número entre 1 y 99 para los Años de uso del Dispositivo'
            )
        else:
            flash(
                f'Ingrese un número entre 1 y 99 para los Años de uso del Dispositivo {index+1}'
            )
    return isValid


def validateSelect(
    select,
    tipo,
    index=-1,
):
    if not select:
        if index == -1:
            flash(f'Seleccione una {tipo}')
        else:
            if index == 0:
                flash(f'Seleccione un {tipo} para el Dispositivo')
            else:
                flash(f'Seleccione un {tipo} para el Dispositivo {index+1}')
        return False
    return True


def validateFiles(files, index):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png", "image/gif", "image/jpg"}

    if files[0].filename == '':
        if index == 0:
            flash('Ningún archivo seleccionado')
        else:
            flash(f'Ningún archivo seleccionado para el Dispositivo {index+1}')
        return False

    if len(files) > 3:
        if index == 0:
            flash('Se permite un máximo de 3 archivos para el Dispositivo')
        else:
            flash(
                f'Se permite un máximo de 3 archivos para el Dispositivo {index+1}'
            )
        return False

    isValid = True

    for image in files:
        # check file extension
        ftype_guess = filetype.guess(image)
        if ftype_guess is None:
            if index == 0:
                flash('Tipo de archivo no permitido para el Dispositivo')
            else:
                flash(
                    f'Tipo de archivo no permitido para el Dispositivo {index}'
                )
            return False

        # check file extension
        if ftype_guess.extension not in ALLOWED_EXTENSIONS:
            if index == 0:
                flash('Tipo de archivo no permitido para el Dispositivo')
            else:
                flash(
                    f'Tipo de archivo no permitido para el Dispositivo {index}'
                )
            isValid = isValid and False

        # check mimetype
        if ftype_guess.mime not in ALLOWED_MIMETYPES:
            if index == 0:
                flash('Tipo de archivo no permitido para el Dispositivo')
            else:
                flash(
                    f'Tipo de archivo no permitido para el Dispositivo {index}'
                )
            isValid = isValid and False

    return isValid


def validate(username, email, number, regiones, comuna, device, deviceType,
             uso, state, images):
    NameisValid = validateName(username)
    EmailisValid = validateEmail(email)
    NumberisValid = validatePhoneNumber(number)
    RegionisValid = validateSelect(regiones, "Región")
    ComunaisValid = validateSelect(comuna, "Comuna")
    DeviceisValid = True
    TypeisValid = True
    UsoisValid = True
    StateisValid = True
    ImagesisValid = True
    for i in range(len(device)):
        DeviceisValid = DeviceisValid and validateName(device[i], i)
        TypeisValid = TypeisValid and validateSelect(deviceType[i], "Tipo", i)
        UsoisValid = UsoisValid and validateUso(uso[i], i)
        StateisValid = StateisValid and validateSelect(
            state[i], "Estado de Funcionamiento", i)
        if i == 0:
            ImagesisValid = ImagesisValid and validateFiles(
                images.getlist('images'), i)
        else:
            ImagesisValid = ImagesisValid and validateFiles(
                images.getlist(f'images-{i+1}'), i)

    return NameisValid and EmailisValid and RegionisValid and \
        ComunaisValid and DeviceisValid and TypeisValid and \
        UsoisValid and StateisValid and NumberisValid
