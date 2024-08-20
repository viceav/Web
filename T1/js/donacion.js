const formContainer = document.getElementById("formContainer");
const formulario = document.getElementById("formulario");

let i = 0;
document.getElementById("agregar").addEventListener("click", () => {
  const form = formulario.cloneNode(true);
  form.id = `new-form-${i}`;
  formContainer.append(form);
  i += 1;
});
