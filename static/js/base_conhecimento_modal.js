// ===============================
// UTILITÁRIO CSRF (OBRIGATÓRIO)
// ===============================
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


// ===============================
// VALIDAÇÃO DE CREDENCIAL
// ===============================
function validarCredencial() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    fetch(`/validar-artigo/${artigoIdAtual}/`, {
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

        // 🔐 garante resposta JSON válida
        const data = await response.json().catch(() => {
            throw new Error("Resposta inválida do servidor");
        });

        console.log("RESPOSTA BACKEND:", data);

        // ✔ SUCESSO → libera artigo
        if (data.ok === true) {

            fecharModal();

            htmx.ajax('GET', `/artigo/${artigoIdAtual}/`, {
                target: "#conteudo-direito",
                swap: "innerHTML"
            });

            return;
        }

        // ❌ ERRO (senha ou permissão)
        document.getElementById("erroSenha").innerText =
            data.erro || "Usuário ou senha inválidos";

    })
    .catch(error => {
        console.error("ERRO FETCH:", error);

        document.getElementById("erroSenha").innerText =
            "Erro de comunicação com o servidor";
    });

    // ===============================
    // ENTER PARA SUBMIT
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

        if (usernameInput) usernameInput.addEventListener("keypress", handleEnter);
        if (passwordInput) passwordInput.addEventListener("keypress", handleEnter);

    });
}