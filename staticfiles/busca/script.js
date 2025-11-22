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

// ===== FILTRO POR BASE =====
document.querySelectorAll('.databases button').forEach(btn => {
  btn.addEventListener('click', () => {
    const base = btn.innerText.toLowerCase();

    let origem = "";
    if (base.includes("pubmed")) origem = "pubmed";
    if (base.includes("scielo")) origem = "scielo";
    if (base.includes("lilacs")) origem = "lilacs";
    if (base.includes("capes")) origem = "capes";

    // pega a URL atual
    const url = new URL(window.location.href);
    const params = url.searchParams;

    // substitui origem
    params.set("origem", origem);

    // redireciona
    window.location.href = `/resultados/?${params.toString()}`;
  });
});

// ===== FILTROS AUTOR/TÍTULO/TEMA =====
document.querySelectorAll('.filters-type button').forEach(btn => {
  btn.addEventListener('click', () => {
    const tipo = btn.innerText.toLowerCase(); // autor / título / tema

    const q = document.querySelector('.search-box input').value.trim();
    if (!q) {
      alert("Digite algo no campo de busca antes de filtrar.");
      return;
    }

    window.location.href = `/resultados/?q=${encodeURIComponent(q)}&tipo=${tipo}`;
  });
});
