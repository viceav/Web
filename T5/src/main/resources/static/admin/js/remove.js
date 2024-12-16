const removeButton = (id, nombre) => {
  const body = document.getElementById("content");
  body.classList.add("overflow-hidden");

  document.getElementById("motivo").innerHTML =
    `Motivo de Eliminación ${nombre}`;

  const div = document.getElementById("popup");
  div.classList.remove("hidden");
  div.classList.add("flex");
  const form = document.getElementById("rm");
  form.action = `/admin/remove?id=${id}`;

  const area = document.getElementById("textarea");
  area.focus();

  const cancel = document.getElementById("cancel");
  cancel.onclick = () => {
    div.classList.remove("flex");
    div.classList.add("hidden");
    body.classList.remove("overflow-hidden");
    area.value = "";
  };
};
