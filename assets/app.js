const D = window.DADOS || {};
const brl = v => v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 });
const $ = s => document.querySelector(s);
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

const gastos = D.gastos || [], viagens = D.viagens || [], entregas = D.entregas || [], meta = D.meta || {};

// Resumo
$('#aviso-exemplo').hidden = !meta.exemplo;
$('#st-gasto').textContent = brl(gastos.reduce((s, g) => s + g.valor, 0));
$('#st-viagens').textContent = viagens.length;
$('#st-paises').textContent = new Set(viagens.filter(v => v.tipo === 'internacional').map(v => v.pais)).size;
$('#st-entregas').textContent = entregas.length;
$('#st-data').textContent = meta.atualizado_em || '—';

// Gastos
const max = Math.max(...gastos.map(g => g.valor), 1);
$('#grafico-gastos').innerHTML = gastos.map((g, i) => `
  <div class="barra" style="height:${(g.valor / max) * 100}%;animation-delay:${i * 40}ms" data-mes="${esc(g.mes.slice(2))}">
    <span class="tip">${brl(g.valor)}</span>
  </div>`).join('');

// Viagens
const mapa = L.map('mapa', { worldCopyJump: true }).setView([-10, -40], 3);
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
  attribution: '&copy; OpenStreetMap &copy; CARTO'
}).addTo(mapa);
const camada = L.layerGroup().addTo(mapa);

function renderViagens(filtro) {
  const lista = viagens.filter(v => filtro === 'todas' || v.tipo === filtro);
  camada.clearLayers();
  lista.forEach(v => L.circleMarker([v.lat, v.lon], {
    radius: 7,
    color: v.tipo === 'internacional' ? '#fdb813' : '#D71920',
    fillColor: v.tipo === 'internacional' ? '#ffffff' : '#ff333d',
    fillOpacity: .9,
    weight: 2
  }).bindPopup(`<b>${esc(v.local)}</b><br>${esc(v.data)}<br>${esc(v.motivo)}`).addTo(camada));
  $('#lista-viagens').innerHTML = lista.map(v => `
    <li><span><strong>${esc(v.local)}</strong> <small>· ${esc(v.motivo)}</small></span>
    <small>${esc(v.data)} · <a href="${esc(v.fonte_url)}" target="_blank" rel="noopener">fonte</a></small></li>`).join('');
}
document.querySelectorAll('.chip').forEach(b => b.addEventListener('click', () => {
  document.querySelectorAll('.chip').forEach(x => x.classList.remove('ativo'));
  b.classList.add('ativo');
  renderViagens(b.dataset.f);
}));
renderViagens('todas');

// Entregas
function renderEntregas(q = '') {
  q = q.toLowerCase();
  $('#grid-entregas').innerHTML = entregas
    .filter(e => [e.titulo, e.area, e.uf].join(' ').toLowerCase().includes(q))
    .map(e => `<article class="card">
      <span class="tag">${esc(e.area)} · ${esc(e.uf)}</span>
      <h3>${esc(e.titulo)}</h3>
      <p>${esc(e.data)}${e.valor ? ' · ' + brl(e.valor) : ''}</p>
      <a href="${esc(e.fonte_url)}" target="_blank" rel="noopener">Ver fonte →</a>
    </article>`).join('') || '<p class="sub">Nada encontrado.</p>';
}
$('#busca-entregas').addEventListener('input', e => renderEntregas(e.target.value));
renderEntregas();
