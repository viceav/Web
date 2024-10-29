fetch("/static/region-comuna.json").then((value) => {
  const regiones = document.getElementById("Regiones");
  const comunas = document.getElementById("Comunas");
  value.json().then((obj) => {
    obj.regiones.forEach((reg) => {
      const option = document.createElement("option");
      option.innerHTML = reg.nombre;
      option.value = `${reg.id}`;
      reg.comunas.forEach((com) => {
        const com_option = document.createElement("option");
        com_option.innerHTML = com.nombre;
        com_option.className = option.value;
        com_option.value = `${com.id}`;
        com_option.hidden = true;
        comunas.append(com_option);
      });
      regiones.append(option);
    });
  }).then(() => {
    const array = Array.from(document.getElementById("Comunas").children)
      .slice(1);
    regiones.addEventListener("change", (elem) => {
      array.forEach((com) => {
        com.hidden = true;
      });
      Array.from(document.getElementsByClassName(`${elem.target.value}`))
        .forEach((com) => {
          com.hidden = false;
        });
    });
  });
});
