// ======================================
// LIMPAR CONTEÚDO DIREITO (BOAS-VINDAS)
// ======================================
function limparConteudo() {
    const conteudoDireito = document.getElementById('conteudo-direito');
    const template = document.getElementById('template-boas-vindas');

    if (conteudoDireito && template) {
        conteudoDireito.innerHTML = template.innerHTML;
    }

    // Remove destaque visual de qualquer link de artigo
    document.querySelectorAll('.article-link').forEach(el => {
        el.classList.remove('highlight-active');
    });
}

// ======================================
// RESTAURAR HOME (FECHA TUDO)
// ======================================
function restaurarHome() {
    limparConteudo();

    document.querySelectorAll('.sidebar details').forEach(detail => {
        detail.removeAttribute('open');
    });

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ======================================
// FUNÇÕES AUXILIARES DE NAVEGAÇÃO
// ======================================

// Fecha o elemento e TODOS os descendentes (filhos e netos)
function fecharRecursivo(elemento) {
    if (!elemento) return;
    elemento.removeAttribute('open');
    elemento.querySelectorAll('details').forEach(child => {
        child.removeAttribute('open');
    });
}

// Fecha apenas as categorias do mesmo nível (irmãs)
function aplicarEfeitoAcordeao(details) {
    const parent = details.parentElement;
    if (!parent) return;

    Array.from(parent.children).forEach(sibling => {
        if (sibling.tagName.toLowerCase() === 'details' && sibling !== details) {
            fecharRecursivo(sibling);
        }
    });
}

// ======================================
// VALIDAÇÃO E CLIQUE DE CATEGORIA
// ======================================
function validarCategoriaClick(event, categoriaId) {
    event.preventDefault();
    event.stopPropagation();

    const details = document.getElementById(`details-cat-${categoriaId}`);
    if (!details) return;

    // AÇÃO: FECHAR
    if (details.hasAttribute("open")) {
        fecharRecursivo(details);
        limparConteudo(); // Volta para boas-vindas ao fechar a categoria
        
        const algumaAberta = document.querySelector('.sidebar details[open]');
        if (!algumaAberta) restaurarHome();
        return;
    }

    // AÇÃO: ABRIR (Verifica restrição)
    const temRestricao = details.dataset.restrita === "true";

    if (!temRestricao) {
        aplicarEfeitoAcordeao(details);
        details.setAttribute("open", "true");
        limparConteudo(); // Limpa o artigo anterior ao trocar de categoria
    } else {
        // Se tem restrição, prepara o modal de senha
        artigoIdAtual = null;
        categoriaIdAtual = categoriaId;
        document.getElementById("modalSenha").style.display = "flex";
    }
}

// ======================================
// LIBERAR CATEGORIA APÓS LOGIN
// ======================================
function liberarCategoriaAposLogin() {
    if (!categoriaIdAtual) return;

    const details = document.querySelector(`#details-cat-${categoriaIdAtual}`);

    if (details) {
        aplicarEfeitoAcordeao(details);
        details.setAttribute("open", "true");
        limparConteudo();
    }

    categoriaIdAtual = null;
}

// ======================================
// VERIFICAR ACESSO AO ARTIGO
// ======================================
function verificarAcessoArtigo(event, artigoId, temRestricao) {
    event.preventDefault();
    event.stopPropagation();

    // Destaque visual no link selecionado
    document.querySelectorAll('.article-link').forEach(el => el.classList.remove('highlight-active'));
    event.target.classList.add('highlight-active');

    // Se não tiver restrição, carrega via HTMX
    if (!temRestricao) {
        htmx.ajax('GET', `/artigo/${artigoId}/`, {
            target: "#conteudo-direito",
            swap: "innerHTML"
        });
        return;
    }

    // Se tiver restrição, abre o modal
    artigoIdAtual = artigoId;
    categoriaIdAtual = null;
    document.getElementById("modalSenha").style.display = "flex";
}

// ======================================
// BUSCA E UTILITÁRIOS
// ======================================
function checkEmptySearch(input) {
    if (input.value.trim() === "") {
        restaurarHome();
    }
}

document.body.addEventListener('htmx:beforeRequest', function(evt) {
    const campoBusca = document.getElementById('campo-busca');
    if (evt.detail.elt === campoBusca && campoBusca.value.trim() === "") {
        evt.preventDefault();
        restaurarHome();
    }
});

// Nota: O listener de click genérico foi removido para evitar conflitos 
// com o onclick="validarCategoriaClick" definido no HTML.