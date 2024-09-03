const agregar = document.getElementById("submit-conf-btn");
const date = new Date();

const validateName = (name) => {
  if (!name) return false;
  let lengthValid = name.trim().length >= 3;
  lengthValid &&= lengthValid <= 80;
  return lengthValid;
};

const validateText = (text) => {
  if (!text) return false;
  let textValid = text.trim().length >= 5;
  return textValid;
};

const agregarComentario = () => {
  let name = document.getElementById("name").value;
  let text = document.getElementById("text").value;

  // variables auxiliares de validación y función.
  let invalidInputs = [];
  let isValid = true;
  const setInvalidInput = (inputName) => {
    invalidInputs.push(inputName);
    isValid &&= false;
  };

  if (!validateName(name)) {
    setInvalidInput("Nombre");
  }
  if (!validateText(text)) {
    setInvalidInput("Texto del Comentario");
  }

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
  } else {
    validationMessageElem.innerText = "Comentario Agregado";
    validationListElem.textContent = "";

    // aplicar estilos de éxito
    validationBox.style.backgroundColor = "#124700";
    validationBox.style.borderLeftColor = "#367D39";
    let commentDiv = document.createElement("div");
    let comments = document.getElementById("Comentarios");
    commentDiv.className = "container";

    let authorP = document.createElement("p");
    let dateSpan = document.createElement("span");
    let textP = document.createElement("p");

    dateSpan.innerHTML =
      `${date.getDay()}/${date.getMonth()}/${date.getFullYear()}`;

    authorP.innerHTML = name;
    authorP.appendChild(dateSpan);
    textP.innerHTML = text;

    commentDiv.appendChild(authorP);
    commentDiv.appendChild(textP);

    comments.insertBefore(commentDiv, comments.firstChild);
    validationBox.hidden = false;
  }
};

agregar.addEventListener("click", () => {
  agregarComentario();
});
