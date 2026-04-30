// static/js/base_conhecimento.js

window.artigoIdAtual = null;
window.categoriaIdAtual = null;

// 1. Configuração Global do HTMX (CSRF Token)
document.body.addEventListener('htmx:configRequest', (event) => {
    const cookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
    if (cookie) {
        event.detail.headers['X-CSRFToken'] = cookie.split('=')[1];
    }
});

// 2. TRATAMENTO DE ERRO 403 (FORBIDDEN)
document.body.addEventListener('htmx:responseError', function(event) {
    if (event.detail.xhr.status === 403) {
        console.warn("Acesso negado pelo servidor. Abrindo modal de senha...");
        document.getElementById("modalSenha").style.display = "flex";
    }
});

// =============================================================================
// CONTROLE DE INTERFACE
// =============================================================================

function limparConteudo() {
    const conteudoDireito = document.getElementById('conteudo-direito');
    const template = document.getElementById('template-boas-vindas');
    if (conteudoDireito && template) {
        conteudoDireito.innerHTML = template.innerHTML;
    }
    document.querySelectorAll('.article-link').forEach(el => el.classList.remove('highlight-active'));
}

function restaurarHome() {
    limparConteudo();
    document.querySelectorAll('.sidebar details').forEach(d => d.removeAttribute('open'));
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function fecharRecursivo(el) {
    if (!el) return;
    el.removeAttribute('open');
    el.querySelectorAll('details').forEach(c => c.removeAttribute('open'));
}

function aplicarEfeitoAcordeao(details) {
    const parent = details.parentElement;
    if (!parent) return;
    Array.from(parent.children).forEach(sibling => {
        if (sibling.tagName.toLowerCase() === 'details' && sibling !== details) {
            fecharRecursivo(sibling);
        }
    });
}

// =============================================================================
// CLIQUES E VALIDAÇÕES
// =============================================================================

function validarCategoriaClick(event, categoriaId) {
    event.preventDefault();
    event.stopPropagation();
    const details = document.getElementById(`details-cat-${categoriaId}`);
    if (!details) return;

    if (details.hasAttribute("open")) {
        fecharRecursivo(details);
        limparConteudo();
        return;
    }

    if (details.dataset.restrita === "false") {
        aplicarEfeitoAcordeao(details);
        details.setAttribute("open", "true");
        limparConteudo();
    } else {
        window.categoriaIdAtual = categoriaId;
        window.artigoIdAtual = null;
        document.getElementById("modalSenha").style.display = "flex";
    }
}

function verificarAcessoArtigo(event, artigoId, temRestricao) {
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }

    window.artigoIdAtual = artigoId;
    window.categoriaIdAtual = null;

    // Estilização visual
    document.querySelectorAll('.article-link').forEach(el => el.classList.remove('highlight-active'));
    const linkAtivo = document.getElementById(`link-artigo-${artigoId}`);
    if (linkAtivo) linkAtivo.classList.add('highlight-active');

    // LÓGICA DE HERANÇA: Se o artigo está dentro de um <details> que já está aberto,
    // assumimos que a categoria pai foi validada e tentamos carregar direto.
    const paiAberto = linkAtivo ? linkAtivo.closest('details[open]') : null;
    const isRestrito = (temRestricao === true || temRestricao === 'True');

    if (!isRestrito || paiAberto) {
        htmx.ajax('GET', `/artigo/${artigoId}/`, {
            target: "#conteudo-direito",
            swap: "innerHTML"
        });
    } else {
        document.getElementById("modalSenha").style.display = "flex";
    }
}

function checkEmptySearch(input) {
    if (input.value.trim() === "") restaurarHome();
}