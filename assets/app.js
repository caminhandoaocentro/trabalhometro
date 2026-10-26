const D = window.DADOS || {};
const $ = s => document.querySelector(s);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

// Formatador BRL completo
const brl = v => {
  if (v == null || isNaN(v)) return '—';
  return Number(v).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 });
};

// Formatador resumido e elegante para grandes números (milhões, bilhões, trilhões)
const brlResumido = v => {
  if (v == null || isNaN(v)) return '—';
  const n = Number(v);
  if (n >= 1e12) return `R$ ${(n / 1e12).toLocaleString('pt-BR', { maximumFractionDigits: 1 })} tri`;
  if (n >= 1e9)  return `R$ ${(n / 1e9).toLocaleString('pt-BR', { maximumFractionDigits: 1 })} bi`;
  if (n >= 1e6)  return `R$ ${(n / 1e6).toLocaleString('pt-BR', { maximumFractionDigits: 1 })} mi`;
  return brl(n);
};

const gastos = D.gastos || [];
const viagens = D.viagens || [];
const entregas = D.entregas || [];
const meta = D.meta || {};

// 1. Resumo / Hero
const avisoEl = $('#aviso-exemplo');
if (avisoEl) {
  if (meta.exemplo) {
    avisoEl.style.display = 'inline-block';
    avisoEl.hidden = false;
  } else {
    avisoEl.style.display = 'none';
    avisoEl.hidden = true;
  }
}

const totalGastos = gastos.reduce((s, g) => s + (Number(g.valor) || 0), 0);
const stGastoEl = $('#st-gasto');
if (stGastoEl) {
  stGastoEl.textContent = brl(totalGastos);
  stGastoEl.title = `Total exato acumulado: ${totalGastos.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`;
}

$('#st-viagens').textContent = viagens.length;
$('#st-paises').textContent = new Set(viagens.filter(v => v.tipo === 'internacional').map(v => v.pais)).size;
$('#st-entregas').textContent = entregas.length;
$('#st-data').textContent = meta.atualizado_em || '—';

// 2. Gráfico de Gastos (Cartão Corporativo)
const graficoEl = $('#grafico-gastos');
if (graficoEl && gastos.length > 0) {
  const max = Math.max(...gastos.map(g => Number(g.valor) || 0), 1);
  graficoEl.innerHTML = gastos.map((g, i) => {
    const valor = Number(g.valor) || 0;
    const [ano, mes] = (g.mes || '----').split('-');
    const rotulo = `${mes}/${ano ? ano.slice(2) : ''}`;
    const alturaPct = Math.max((valor / max) * 100, 4);
    const transTxt = g.transacoes ? `<br><small style="color:var(--mut);font-weight:400">${g.transacoes} transações</small>` : '';

    return `
      <div class="barra" style="height:${alturaPct}%;animation-delay:${Math.min(i * 12, 500)}ms" data-mes="${esc(rotulo)}">
        <span class="tip">
          <strong>${esc(rotulo)}:</strong> ${brl(valor)}
          ${transTxt}
        </span>
      </div>`;
  }).join('');
}

// 3. Viagens e Mapa
let mapa;
try {
  mapa = L.map('mapa', { worldCopyJump: true }).setView([-12, -45], 3);
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap &copy; CARTO'
  }).addTo(mapa);

  // Corrige renderização de tiles
  setTimeout(() => { mapa.invalidateSize(); }, 300);
} catch (e) {
  console.warn('Erro ao carregar Leaflet:', e);
}

const camada = mapa ? L.layerGroup().addTo(mapa) : null;

function renderViagens(filtro) {
  const lista = viagens.filter(v => filtro === 'todas' || v.tipo === filtro);

  if (camada) {
    camada.clearLayers();
    lista.forEach(v => {
      if (v.lat != null && v.lon != null) {
        L.circleMarker([v.lat, v.lon], {
          radius: 7,
          color: v.tipo === 'internacional' ? '#fdb813' : '#D71920',
          fillColor: v.tipo === 'internacional' ? '#ffffff' : '#ff3843',
          fillOpacity: 0.9,
          weight: 2
        }).bindPopup(`
          <div style="font-family:Inter,sans-serif;color:#111">
            <strong style="font-size:1.05rem;color:#BA0C2F">${esc(v.local)}</strong> (${esc(v.pais || 'Brasil')})<br>
            <small style="color:#666">${esc(v.data)}</small>
            <p style="margin:4px 0 0;font-size:0.85rem">${esc(v.motivo || '')}</p>
          </div>
        `).addTo(camada);
      }
    });
  }

  const listaEl = $('#lista-viagens');
  if (listaEl) {
    listaEl.innerHTML = lista.map(v => `
      <li>
        <div>
          <strong>${esc(v.local)}</strong>
          <small style="color:var(--pt-white);opacity:.8"> (${esc(v.pais || 'Brasil')})</small>
          <br>
          <small style="color:var(--mut)">${esc(v.motivo || 'Viagem oficial')}</small>
        </div>
        <div style="text-align:right;white-space:nowrap">
          <small style="display:block;color:var(--mut)">${esc(v.data)}</small>
          <a href="${esc(v.fonte_url)}" target="_blank" rel="noopener">Fonte →</a>
        </div>
      </li>
    `).join('') || '<li style="color:var(--mut)">Nenhuma viagem encontrada para este filtro.</li>';
  }
}

document.querySelectorAll('.chip').forEach(b => b.addEventListener('click', () => {
  document.querySelectorAll('.chip').forEach(x => x.classList.remove('ativo'));
  b.classList.add('ativo');
  renderViagens(b.dataset.f);
}));

renderViagens('todas');

// 4. Entregas e Busca
function renderEntregas(q = '') {
  q = q.toLowerCase();
  const lista = entregas.filter(e =>
    [e.titulo, e.area, e.uf, e.descricao || ''].join(' ').toLowerCase().includes(q)
  );

  const gridEl = $('#grid-entregas');
  if (!gridEl) return;

  gridEl.innerHTML = lista.map(e => {
    const valorTxt = e.valor ? ` · <strong>${brlResumido(e.valor)}</strong>` : '';
    const descTxt = e.descricao ? `<p class="desc">${esc(e.descricao)}</p>` : '';
    return `
      <article class="card">
        <div>
          <span class="tag">${esc(e.area)} · ${esc(e.uf)}</span>
          <h3>${esc(e.titulo)}</h3>
          ${descTxt}
        </div>
        <div>
          <p class="meta-entrega">${esc(e.data)}${valorTxt}</p>
          <a href="${esc(e.fonte_url)}" target="_blank" rel="noopener">Ver documento oficial →</a>
        </div>
      </article>`;
  }).join('') || '<p class="sub" style="grid-column: 1 / -1; text-align: center; padding: 2rem;">Nenhuma entrega encontrada com esse termo.</p>';
}

const buscaInput = $('#busca-entregas');
if (buscaInput) {
  buscaInput.addEventListener('input', e => renderEntregas(e.target.value));
}

renderEntregas();
