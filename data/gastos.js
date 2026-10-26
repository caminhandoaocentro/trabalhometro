// EXEMPLO FICTÍCIO — substituir pela saída do script Python.
// Campos: mes (AAAA-MM), valor (R$), fonte_url
window.DADOS = window.DADOS || {};
window.DADOS.gastos = [
  "2026-01","2026-02","2026-03","2026-04","2026-05","2026-06",
  "2026-07","2026-08","2026-09"
].map((mes, i) => ({ mes, valor: 100000 + i * 15000, fonte_url: "https://portaldatransparencia.gov.br/cartoes" }));
