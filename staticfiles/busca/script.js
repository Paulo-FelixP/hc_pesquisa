// =========================
// Funções utilitárias
// =========================
function qs(sel, ctx = document) { 
    return ctx.querySelector(sel); 
}
function qsa(sel, ctx = document) { 
    return Array.from(ctx.querySelectorAll(sel)); 
}

// ============================================================================
// MENU LATERAL (só existe na página de busca — protegido com IF)
// ============================================================================
const menuBtn = qs('#menuBtn');
const sidebar = qs('#sidebar');

if (menuBtn && sidebar) {
    menuBtn.addEventListener('click', () => {
        sidebar.classList.toggle('active');
    });

    document.addEventListener('click', (e) => {
        if (!sidebar.contains(e.target) && !menuBtn.contains(e.target)) {
            sidebar.classList.remove('active');
        }
    });
} else {
    console.debug("[OK] menuBtn/sidebar não existem nesta página.");
}

// ============================================================================
// MULTI-SELEÇÃO DE BASES (só existe na página principal)
// ============================================================================
if (qsa('.databases button').length > 0) {
    let origensSelecionadas = [];

    qsa('.databases button').forEach(btn => {
        btn.addEventListener('click', () => {
            const base = btn.dataset.base;

            if (origensSelecionadas.includes(base)) {
                origensSelecionadas = origensSelecionadas.filter(b => b !== base);
                btn.classList.remove("active");
            } else {
                origensSelecionadas.push(base);
                btn.classList.add("active");
            }

            const hidden = qs("#origens_input");
            if (hidden) hidden.value = origensSelecionadas.join(",");
        });
    });

    console.debug("[OK] Multi-seleção ativada.");
} else {
    console.debug("[OK] Não há multi-seleção nesta página.");
}

// ============================================================================
// TIPO (autor/título/tema) — só na página principal
// ============================================================================
if (qsa('.filters-type button').length > 0) {
    qsa('.filters-type button').forEach(btn => {
        btn.addEventListener('click', () => {
            qsa('.filters-type button')
                .forEach(x => x.classList.remove("active"));

            btn.classList.add("active");

            const hidden = qs("#tipo_input");
            if (hidden) hidden.value = btn.dataset.tipo;
        });
    });

    console.debug("[OK] Tipos configurados.");
} else {
    console.debug("[OK] Não há filtros tipo.");
}

// ============================================================================
// BOTÃO PESQUISAR — só existe na página principal
// ============================================================================
const btnPesquisar = qs("#btnPesquisar");
if (btnPesquisar) {
    btnPesquisar.addEventListener("click", () => {
        const form = qs("form");
        if (form) form.submit();
    });

    console.debug("[OK] Botão Pesquisar configurado.");
} else {
    console.debug("[OK] Página sem botão Pesquisar.");
}

// ============================================================================
// ============================================================================
// A PARTIR DAQUI — CÓDIGO DA PÁGINA RESULTADOS
// ============================================================================
// ============================================================================

// Abrir modal
function abrirModalComDados(d) {
    const modal = qs('#planilhaModal');
    if (!modal) return;

    const info = qs('#modalArticleInfo');
    if (info) {
        let resumo = d.titulo || '(sem título)';
        if (d.autores) resumo += ' — ' + d.autores;
        info.textContent = resumo;
    }

    const map = {
        h_titulo: d.titulo,
        h_autores: d.autores,
        h_resumo: (d.resumo || '').substring(0, 800),
        h_data: d.data,
        h_origem: d.origem,
        h_link: d.link,
    };

    for (const id in map) {
        const el = qs('#' + id);
        if (el) el.value = map[id] || '';
    }

    qsa('#listaPlanilhas .item-planilha')
        .forEach(x => x.classList.remove('selecionada'));

    const btnAdd = qs('#btnAdicionarSelecionada');
    if (btnAdd) btnAdd.disabled = true;

    modal.style.display = 'flex';
    modal.setAttribute('aria-hidden', 'false');
}

function fecharModal() {
    const modal = qs('#planilhaModal');
    if (!modal) return;

    modal.style.display = 'none';
    modal.setAttribute('aria-hidden', 'true');
}

// Inicialização final
document.addEventListener('DOMContentLoaded', () => {

    console.log("[OK] script.js carregado");

    // Botões "Planilha"
    qsa('button.planilha-btn').forEach(btn => {
        btn.addEventListener('click', (ev) => {
            ev.preventDefault();

            const d = {
                titulo: btn.dataset.titulo  || '',
                autores: btn.dataset.autores || '',
                resumo: btn.dataset.resumo  || '',
                data: btn.dataset.data || '',
                link: btn.dataset.link || '',
                origem: btn.dataset.origem || '',
            };

            abrirModalComDados(d);
        });
    });

    // Botão fechar modal
    const btnClose = qs('#btnFecharModal');
    if (btnClose) {
        btnClose.addEventListener('click', (e) => {
            e.preventDefault();
            fecharModal();
        });
    }

    // Seleção de planilha
    qsa('#listaPlanilhas .item-planilha').forEach(item => {
        item.addEventListener('click', () => {
            qsa('#listaPlanilhas .item-planilha')
                .forEach(x => x.classList.remove('selecionada'));

            item.classList.add('selecionada');

            const btnAdd = qs('#btnAdicionarSelecionada');
            if (btnAdd) btnAdd.disabled = false;
        });
    });

    // Botão adicionar na planilha
    const botaoAdd = qs('#btnAdicionarSelecionada');
    if (botaoAdd) {
        botaoAdd.addEventListener('click', (e) => {
            e.preventDefault();

            const selecionada = qs('#listaPlanilhas .item-planilha.selecionada');
            if (!selecionada) return alert('Selecione uma planilha primeiro.');

            const planilhaId = selecionada.dataset.id;
            const formAdd = qs('#formAdicionarItem');

            if (formAdd) {
                formAdd.action = `/planilhas/${planilhaId}/adicionar/`;
                formAdd.submit();
            }
        });
    }
});
