var hashUsuario = document.getElementById("hashUsuario").value;
var hash = "hash";
sessionStorage.setItem(hash, hashUsuario);
console.log(sessionStorage.getItem(hash));
