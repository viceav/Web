const image = document.getElementById("celu");
const full = document.getElementById("full");
const body = document.body;

image.addEventListener("click", () => {
  full.toggleAttribute("hidden");
  body.style = "overflow: hidden;";
});

full.addEventListener("click", () => {
  full.toggleAttribute("hidden");
  body.style = "overflow: auto;";
});
