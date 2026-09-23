const saklar = document.getElementById("saklar");
const status = document.getElementById("status");

saklar.addEventListener("change", () => {
  if (saklar.checked) {
    document.body.classList.add("dark")
  } else {
    document.body.classList.remove("dark")
  }
});