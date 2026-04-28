// ===============================
// UTILITÁRIO CSRF
// ===============================
function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }

    return cookieValue;
}


// ===============================
// VALIDAÇÃO DE CREDENCIAL
// ===============================
function validarCredencial() {

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const erroSenha = document.getElementById("erroSenha"); 

    let url = "";

    if (artigoIdAtual) {
        url = `/validar-artigo/${artigoIdAtual}/`;
    } else if (categoriaIdAtual) {
        url = `/validar-categoria/${categoriaIdAtual}/`;
    } else {
        erroSenha.innerText = "Erro interno";
        erroSenha.style.display = "block";
        return;
    }

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: new URLSearchParams({
            username: username,
            password: password
        })
    })
    .then(async response => {

        const data = await response.json();

        if (data.ok === true) {
            fecharModal();

            if (categoriaIdAtual && typeof liberarCategoriaAposLogin === "function") {
                liberarCategoriaAposLogin();
            }

            if (artigoIdAtual) {
                htmx.ajax('GET', `/artigo/${artigoIdAtual}/`, {
                    target: "#conteudo-direito",
                    swap: "innerHTML"
                });
            }
            return;
        }

        erroSenha.innerText = data.erro || "Usuário ou senha inválidos";
        erroSenha.style.display = "block"; 

    })
    .catch((err) => {
        console.error("ERRO:", err);
        erroSenha.innerText = "Erro de comunicação com o servidor";
        erroSenha.style.display = "block";
    });
}


// ===============================
// ENTER NO MODAL
// ===============================
document.addEventListener("DOMContentLoaded", function () {

    function handleEnter(e) {
        if (e.key === "Enter") {
            e.preventDefault();
            validarCredencial();
        }
    }

    const usernameInput = document.getElementById("username");
    const passwordInput = document.getElementById("password");

    if (usernameInput) {
        usernameInput.addEventListener("keypress", handleEnter);
    }

    if (passwordInput) {
        passwordInput.addEventListener("keypress", handleEnter);
    }

});