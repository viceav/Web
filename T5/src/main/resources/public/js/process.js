const processButton = (desc) => {
  desc = desc.split("-");
  const attr = desc[0];
  let id = parseInt(desc[1]);

  const cnt = document.getElementById(`${attr}-${id}`);
  cnt.innerHTML = parseInt(cnt.innerHTML) + 1;

  fetch(`/update?attr=${attr}&id=${id}`, {
    method: "POST",
    credentials: "include",
  });
};
