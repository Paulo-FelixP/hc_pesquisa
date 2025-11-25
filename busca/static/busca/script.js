// Alternar o menu lateral
const menuBtn = document.getElementById('menuBtn');
const sidebar = document.getElementById('sidebar');

menuBtn.addEventListener('click', () => {
  sidebar.classList.toggle('active');
});

// Fechar menu ao clicar fora
document.addEventListener('click', (e) => {
  if (!sidebar.contains(e.target) && !menuBtn.contains(e.target)) {
    sidebar.classList.remove('active');
  }
});

// ===== MULTI-SELEÇÃO DE BASES =====
let origensSelecionadas = [];

document.querySelectorAll('.databases button').forEach(btn => {
  btn.addEventListener('click', () => {

    const base = btn.dataset.base;

    // alterna seleção
    if (origensSelecionadas.includes(base)) {
      origensSelecionadas = origensSelecionadas.filter(b => b !== base);
      btn.classList.remove("active");
    } else {
      origensSelecionadas.push(base);
      btn.classList.add("active");
    }

    // coloca no hidden
    document.getElementById("origens_input").value = origensSelecionadas.join(",");
  });
});

// ===== TIPO (autor/título/tema) =====
document.querySelectorAll('.filters-type button').forEach(btn => {
  btn.addEventListener('click', () => {

    // remove seleção anterior
    document.querySelectorAll('.filters-type button')
      .forEach(x => x.classList.remove("active"));

    btn.classList.add("active");

    document.getElementById("tipo_input").value = btn.dataset.tipo;
  });
});

// ===== BOTÃO PESQUISAR =====
// agora SÓ envia quando clicar nele
document.getElementById("btnPesquisar").addEventListener("click", () => {
  document.querySelector("form").submit();
});
