const menubutton = document.getElementById("hamburger");
const sidebar = document.getElementById("sidebar")

menubutton.addEventListener("click", ()=>{ sidebar.classList.toggle("active"); });