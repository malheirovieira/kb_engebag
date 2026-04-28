function limparConteudo() {
    const conteudoDireito = document.getElementById('conteudo-direito');
    const template = document.getElementById('template-boas-vindas');

    if (conteudoDireito && template) {
        conteudoDireito.innerHTML = template.innerHTML;
    }

    document.querySelectorAll('.article-link').forEach(el => {
        el.classList.remove('highlight-active');
    });
}

function restaurarHome() {
    limparConteudo();

    document.querySelectorAll('.sidebar details').forEach(detail => {
        detail.removeAttribute('open');
    });

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

document.addEventListener('click', function(e) {

    const trigger = e.target.closest('.module-card');

    if (!trigger) return;

    e.preventDefault();
    e.stopPropagation();

    const details = trigger.closest('details');

    if (!details) return;

    if (details.hasAttribute('open')) {

        limparConteudo();

        details.removeAttribute('open');
        details.querySelectorAll('details').forEach(child => {
            child.removeAttribute('open');
        });

        const algumaAberta = document.querySelector('.sidebar details[open]');
        if (!algumaAberta) {
            restaurarHome();
        }

    } else {

        const isRaiz = !details.parentElement.closest('details');

        if (isRaiz) {
            document.querySelectorAll('.sidebar > .modules > details').forEach(el => {
                el.removeAttribute('open');
                el.querySelectorAll('details').forEach(sub => sub.removeAttribute('open'));
            });
            restaurarHome();
        } else {
            const parentContainer = details.parentElement;

            Array.from(parentContainer.children).forEach(sibling => {
                if (sibling.tagName.toLowerCase() === 'details' && sibling !== details) {
                    sibling.removeAttribute('open');
                    sibling.querySelectorAll('details').forEach(sub => sub.removeAttribute('open'));
                }
            });
        }

        details.querySelectorAll('details').forEach(child => {
            child.removeAttribute('open');
        });

        limparConteudo();
        details.setAttribute('open', 'true');
    }
});

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