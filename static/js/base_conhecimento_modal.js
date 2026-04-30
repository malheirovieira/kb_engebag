// static/js/base_conhecimento_modal.js

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function fecharModal() {
    const modal = document.getElementById("modalSenha");
    if (modal) modal.style.display = "none";
    document.getElementById("username").value = "";
    document.getElementById("password").value = "";
    const erroElem = document.getElementById("erroSenha");
    if (erroElem) {
        erroElem.innerText = "";
        erroElem.style.display = "none";
    }
}

function liberarAcessoAposLogin() {
    if (window.categoriaIdAtual) {
        const details = document.getElementById(`details-cat-${window.categoriaIdAtual}`);
        if (details) {
            if (typeof aplicarEfeitoAcordeao === "function") {
                aplicarEfeitoAcordeao(details);
            }
            details.setAttribute("open", "true");
        }
    } 
    
    if (window.artigoIdAtual) {
        htmx.ajax('GET', `/artigo/${window.artigoIdAtual}/`, {
            target: "#conteudo-direito",
            swap: "innerHTML"
        });
    }
    
    fecharModal();
    
    setTimeout(() => {
        window.artigoIdAtual = null;
        window.categoriaIdAtual = null;
    }, 300);
}

function validarCredencial() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const erroSenha = document.getElementById("erroSenha"); 

    if (!username || !password) {
        erroSenha.innerText = "Informe usuário e senha.";
        erroSenha.style.display = "block";
        return;
    }

    let url = window.artigoIdAtual ? `/validar-artigo/${window.artigoIdAtual}/` : `/validar-categoria/${window.categoriaIdAtual}/`;

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: new URLSearchParams({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.ok) {
            liberarAcessoAposLogin();
        } else {
            erroSenha.innerText = data.erro || "Credenciais inválidas";
            erroSenha.style.display = "block";
        }
    })
    .catch((err) => {
        console.error("Erro no Fetch:", err);
        erroSenha.innerText = "Erro ao processar login.";
        erroSenha.style.display = "block";
    });
}

document.addEventListener("DOMContentLoaded", function () {
    const pwdInput = document.getElementById("password");
    if (pwdInput) {
        pwdInput.addEventListener("keypress", function(e) {
            if (e.key === "Enter") {
                e.preventDefault();
                validarCredencial();
            }
        });
    }
});