const submit = document.getElementById("publicar");

const validateName = (name) => {
  if (!name) return false;
  let lengthValid = name.trim().length >= 3;
  lengthValid &&= lengthValid <= 80;
  return lengthValid;
};

const validateEmail = (email) => {
  if (!email) return false;

  // validamos el formato
  let re = /^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
  let formatValid = re.test(email);

  // devolvemos la lógica AND de las validaciones.
  return formatValid;
};

const validatePhoneNumber = (phoneNumber) => {
  if (phoneNumber != "") {
    // validación de longitud
    let lengthValid = phoneNumber.length >= 8;

    // validación de formato
    let re = /^[0-9]+$/;
    let formatValid = re.test(phoneNumber);

    // devolvemos la lógica AND de las validaciones.
    return lengthValid && formatValid;
  } else return true;
};

const validateUso = (uso) => {
  let lengthValid = uso.trim().length > 0;
  lengthValid &&= lengthValid <= 2;
  return lengthValid && !isNaN(uso);
};

const validateSelect = (select) => {
  if (!select) return false;
  return true;
};

const validateFiles = (files) => {
  if (!files) return false;

  // validación del número de archivos
  let lengthValid = 1 <= files.length && files.length <= 3;

  // validación del tipo de archivo
  let typeValid = true;

  for (const file of files) {
    // el tipo de archivo debe ser "image/<foo>" o "application/pdf"
    let fileFamily = file.type.split("/")[0];
    typeValid &&= fileFamily == "image";
  }

  // devolvemos la lógica AND de las validaciones.
  return lengthValid && typeValid;
};

const validateForm = () => {
  // obtener elementos del DOM usando el nombre del formulario.
  let myForm = document.getElementById("form");
  let name = myForm["username"].value;
  let email = myForm["email"].value;
  let phoneNumber = myForm["number"].value;
  let regiones = myForm["Regiones"].value;
  let comunas = myForm["Comunas"].value;
  let device = myForm["device"];
  let tipo = myForm["type"];
  let uso = myForm["use"];
  let estado = myForm["state"];

  // variables auxiliares de validación y función.
  let invalidInputs = [];
  let isValid = true;
  const setInvalidInput = (inputName) => {
    invalidInputs.push(inputName);
    isValid &&= false;
  };

  // lógica de validación
  if (!validateName(name)) {
    setInvalidInput("Nombre Donante");
  }
  if (!validateEmail(email)) {
    setInvalidInput("Email Donante");
  }
  if (!validatePhoneNumber(phoneNumber)) {
    setInvalidInput("Ingrese un número de celular válido");
  }
  if (!validateSelect(regiones)) {
    setInvalidInput("Región del Donante");
  }
  if (!validateSelect(comunas)) {
    setInvalidInput("Comuna del Donante");
  }

  const isIterable = (obj) => {
    return typeof obj[Symbol.iterator] === "function";
  };

  // Si no es iterable lo accedemos solo al valor
  if (!isIterable(device)) {
    let files = myForm["images"];
    if (!validateName(device.value)) {
      setInvalidInput(`Nombre del Dispositivo`);
    }
    if (!validateSelect(tipo.value)) {
      setInvalidInput(`Tipo de Dispositivo`);
    }
    if (!validateUso(uso.value)) {
      setInvalidInput(`Años de Uso del dispositivo`);
    }
    if (!validateSelect(estado.value)) {
      setInvalidInput(`Estado de funcionamiento del Dispositivo`);
    }
    if (!validateFiles(files.files)) {
      let message = "Fotos de productos: ";
      message += `Se requieren de 1 a 3 fotos para el Dispositivo`;
      setInvalidInput(message);
    }
  } // Si es iterable vamos iterando para validar cada dispositivo
  else {
    device.forEach((_, i) => {
      let files;
      if (i == 0) {
        files = myForm["images"];
      } else {
        files = myForm[`images-${i + 1}`];
      }
      if (!validateName(device[i].value)) {
        setInvalidInput(
          i == 0 ? `Nombre del Dispositivo` : `Nombre del Dispositivo ${i + 1}`,
        );
      }
      if (!validateSelect(tipo[i].value)) {
        setInvalidInput(
          i == 0 ? `Tipo de Dispositivo` : `Tipo de Dispositivo ${i + 1}`,
        );
      }
      if (!validateUso(uso[i].value)) {
        setInvalidInput(
          i == 0
            ? `Años de Uso del dispositivo`
            : `Años de Uso del Dispositivo ${i + 1}`,
        );
      }
      if (!validateSelect(estado[i].value)) {
        setInvalidInput(
          i == 0
            ? `Estado de funcionamiento del Dispositivo`
            : `Estado de funcionamiento del Dispositivo ${i + 1}`,
        );
      }
      if (!validateFiles(files.files)) {
        let message = "Fotos de productos: ";
        i == 0
          ? message += `Se requieren de 1 a 3 fotos para el Dispositivo`
          : message += `Se requieren de 1 a 3 fotos para el Dispositivo ${
            i + 1
          }`, setInvalidInput(message);
      }
    });
  }
  // finalmente mostrar la validación
  let validationBox = document.getElementById("val-box");
  let validationMessageElem = document.getElementById("val-msg");
  let validationListElem = document.getElementById("val-list");

  if (!isValid) {
    validationListElem.textContent = "";
    // agregar elementos inválidos al elemento val-list.
    for (input of invalidInputs) {
      let listElement = document.createElement("li");
      listElement.innerText = input;
      validationListElem.append(listElement);
    }
    // establecer val-msg
    validationMessageElem.innerText = "Los siguientes campos son inválidos:";

    // aplicar estilos de error
    validationBox.style.backgroundColor = "#470000";
    validationBox.style.borderLeftColor = "#9D1309";

    // hacer visible el mensaje de validación
    validationBox.hidden = false;
    window.scrollTo({ top: 0 });
  } else {
    // Ocultar el formulario
    document.getElementById("link").hidden = true;
    myForm.style.display = "none";

    // establecer mensaje de éxito
    validationMessageElem.innerText =
      "Confirma que desea publicar esta donación?";
    validationListElem.textContent = "";

    // aplicar estilos de éxito
    validationBox.style.backgroundColor = "#124700";
    validationBox.style.borderLeftColor = "#367D39";

    // Agregar botones para enviar el formulario o volver
    let submitButton = document.createElement("button");
    submitButton.innerText = "Sí, confirmo";
    submitButton.style.marginRight = "10px";
    submitButton.addEventListener("click", () => {
      myForm.submit();
    });

    let backButton = document.createElement("button");
    backButton.innerText = "No, quiero volver al formulario";
    backButton.addEventListener("click", () => {
      document.getElementById("link").hidden = false;
      // Mostrar el formulario nuevamente
      myForm.style.display = "block";
      validationBox.hidden = true;
    });

    validationListElem.appendChild(submitButton);
    validationListElem.appendChild(backButton);

    // hacer visible el mensaje de validación
    validationBox.hidden = false;
  }
};
submit.addEventListener("click", () => {
  validateForm();
});
