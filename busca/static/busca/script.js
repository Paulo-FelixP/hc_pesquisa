// =========================
// Funções utilitárias
// =========================
function qs(sel, ctx = document) { return ctx.querySelector(sel); }
function qsa(sel, ctx = document) { return Array.from((ctx || document).querySelectorAll(sel)); }

console.debug("[script.js] carregando...");

// menu lateral defensivo
const menuBtn = qs('#menuBtn');
const sidebar = qs('#sidebar');
if (menuBtn && sidebar) {
  menuBtn.addEventListener('click', () => sidebar.classList.toggle('active'));
  document.addEventListener('click', (e) => {
    if (!sidebar.contains(e.target) && !menuBtn.contains(e.target)) sidebar.classList.remove('active');
  });
}

// Inicia quando DOM pronto
document.addEventListener('DOMContentLoaded', () => {
  console.debug("[script.js] DOM pronto");

  // Botões "Planilha" presentes em cada resultado
  qsa('button.planilha-btn').forEach(btn => {
    btn.addEventListener('click', (ev) => {
      ev.preventDefault();
      const d = {
        // tentamos dataset primeiro, se não existe pegamos atributo (compatibilidade)
        titulo: btn.dataset.titulo || btn.getAttribute('data-titulo') || '',
        autores: btn.dataset.autores || btn.getAttribute('data-autores') || '',
        resumo: btn.dataset.resumo || btn.getAttribute('data-resumo') || '',
        data_publicacao: btn.dataset.data || btn.getAttribute('data-data') || '',
        link: btn.dataset.link || btn.getAttribute('data-link') || '',
        origem: btn.dataset.origem || btn.getAttribute('data-origem') || '',
      };
      abrirModalComDadosObj(d);
    });
  });

  // fechar modal
  const btnClose = qs('#btnFecharModal');
  if (btnClose) btnClose.addEventListener('click', (e) => { e.preventDefault(); fecharModalPlanilha(); });

  // seleção de planilha na lista
  qsa('#listaPlanilhas .item-planilha').forEach(item => {
    item.addEventListener('click', () => {
      qsa('#listaPlanilhas .item-planilha').forEach(x => x.classList.remove('selecionada'));
      item.classList.add('selecionada');
      const btnAdd = qs('#btnAdicionarSelecionada');
      if (btnAdd) btnAdd.disabled = false;
    });
  });

  // adicionar à planilha selecionada (envia o form oculto)
  const btnAdicionar = qs('#btnAdicionarSelecionada');
  if (btnAdicionar) {
    btnAdicionar.addEventListener('click', (e) => {
      e.preventDefault();
      const selecionada = qs('#listaPlanilhas .item-planilha.selecionada');
      if (!selecionada) { alert('Selecione uma planilha primeiro.'); return; }
      const planilhaId = selecionada.dataset.id;
      const formAdd = qs('#formAdicionarItem');
      if (!formAdd) { alert('Formulário não encontrado. Recarregue a página.'); return; }

      // Debug: confirma que os campos hidden foram preenchidos
      console.debug("[planilha] hidden titulo:", qs('#h_titulo')?.value);

      formAdd.action = `/planilhas/${planilhaId}/adicionar/`;
      console.debug(`[planilha] Submetendo para ${formAdd.action}`);
      formAdd.submit();
    });
  }

}); // DOMContentLoaded

// ---- funções que também podem ser chamadas fora do DOMContentLoaded ----
function abrirModalComDadosObj(d) {
  const modal = qs('#planilhaModal');
  if (!modal) { console.warn("[planilha] modal não encontrado"); return; }

  const info = qs('#modalArticleInfo');
  if (info) {
    let resumo = d.titulo || '(sem título)';
    if (d.autores) resumo += ' — ' + d.autores;
    info.textContent = resumo;
  }

  // preencher os hidden inputs (note os IDs)
  const setIf = (id, val) => {
    const el = qs('#' + id);
    if (el) el.value = val || '';
  };
  setIf('h_titulo', d.titulo || '');
  setIf('h_autores', d.autores || '');
  setIf('h_resumo', (d.resumo || '').substring(0, 2000));
  setIf('h_data', d.data_publicacao || '');
  setIf('h_origem', d.origem || '');
  setIf('h_link', d.link || '');

  // limpar seleção
  qsa('#listaPlanilhas .item-planilha').forEach(x => x.classList.remove('selecionada'));
  const btnAdd = qs('#btnAdicionarSelecionada'); if (btnAdd) btnAdd.disabled = true;

  modal.style.display = 'flex';
  modal.setAttribute('aria-hidden', 'false');
}

function fecharModalPlanilha() {
  const modal = qs('#planilhaModal');
  if (!modal) return;
  modal.style.display = 'none';
  modal.setAttribute('aria-hidden', 'true');
}
