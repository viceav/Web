const devices = document.getElementById("Devices");
const device = document.getElementById("device-0");

let i = 1;
const button = document.getElementById("agregar");
button.addEventListener("click", () => {
  const newDevice = device.cloneNode(true);
  newDevice.id = `device-${i}`;
  i += 1;
  newDevice.childNodes[1].innerHTML = `Nombre Dispositivo ${i}`;
  newDevice.children["images"].name = `images-${i}`;
  button.before(newDevice);
});
