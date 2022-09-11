var mostrar = document.getElementById("hashUsuarioO");
var hashUsuario = sessionStorage.getItem(hash);
console.log(hashUsuario);
mostrar.value = hashUsuario;
