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
const destaqueBoxEl = $('#destaque-gastos-box');
const containerScroll = $('#barras-scroll-container');
const graficoEl = $('#grafico-gastos');

if (gastos.length > 0) {
  // Último mês consolidado
  const ultimoGasto = gastos[gastos.length - 1];
  const [uAno, uMes] = (ultimoGasto.mes || '').split('-');
  const mesesNomes = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'];
  const nomeMesExtenso = mesesNomes[parseInt(uMes, 10) - 1] || uMes;
  const mediaMensal = totalGastos / gastos.length;

  if (destaqueBoxEl) {
    destaqueBoxEl.innerHTML = `
      <div class="destaque-mini">
        <div class="rotulo">Último Mês Disponível (CGU)</div>
        <div class="valor-destaque">${brl(ultimoGasto.valor)}</div>
        <div class="detalhe">📅 ${nomeMesExtenso}/${uAno} · ${ultimoGasto.transacoes || 0} transações</div>
      </div>
      <div class="destaque-mini">
        <div class="rotulo">Média Mensal Oficial</div>
        <div class="valor-destaque">${brl(mediaMensal)}</div>
        <div class="detalhe">Base de 44 meses catalogados</div>
      </div>
      <div class="destaque-mini">
        <div class="rotulo">Total Acumulado (Mandato)</div>
        <div class="valor-destaque">${brlResumido(totalGastos)}</div>
        <div class="detalhe">Cartão de Pagamento do Gov. Federal</div>
      </div>
    `;
  }

  function renderGrafico(filtroAno = 'todos') {
    const listaFiltrada = gastos.filter(g => {
      if (filtroAno === 'todos') return true;
      return (g.mes || '').startsWith(filtroAno);
    });

    if (!graficoEl) return;
    const max = Math.max(...listaFiltrada.map(g => Number(g.valor) || 0), 1);

    graficoEl.style.minWidth = filtroAno === 'todos' ? '920px' : '100%';
    graficoEl.innerHTML = listaFiltrada.map((g, i) => {
      const valor = Number(g.valor) || 0;
      const [ano, mes] = (g.mes || '----').split('-');
      const rotulo = `${mes}/${ano ? ano.slice(2) : ''}`;
      const alturaPct = Math.max((valor / max) * 100, 5);
      const transTxt = g.transacoes ? `<br><small style="color:var(--mut);font-weight:400">${g.transacoes} transações</small>` : '';

      return `
        <div class="barra" style="height:${alturaPct}%;animation-delay:${Math.min(i * 12, 400)}ms" data-mes="${esc(rotulo)}">
          <span class="tip">
            <strong>${esc(rotulo)}:</strong> ${brl(valor)}
            ${transTxt}
          </span>
        </div>`;
    }).join('');

    // Rola automaticamente para os meses mais recentes à direita
    if (containerScroll) {
      setTimeout(() => {
        containerScroll.scrollTo({ left: containerScroll.scrollWidth, behavior: 'smooth' });
      }, 100);
    }
  }

  // Eventos dos filtros por ano
  document.querySelectorAll('.chip-ano').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.chip-ano').forEach(b => b.classList.remove('ativo'));
      btn.classList.add('ativo');
      renderGrafico(btn.dataset.ano);
    });
  });

  renderGrafico('todos');
}

// 3. Viagens e Mapa
let mapa;
try {
  mapa = L.map('mapa', {
    worldCopyJump: true,
    minZoom: 2,
    maxZoom: 16
  }).setView([-14, -51], 3);

  // Mapa escuro oficial sem marca d'água (Esri World Dark Gray Canvas)
  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
    attribution: '&copy; Esri &copy; OpenStreetMap',
    maxZoom: 16
  }).addTo(mapa);

  // Linhas e referências de países sutis
  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Reference/MapServer/tile/{z}/{y}/{x}', {
    maxZoom: 16,
    opacity: 0.85
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
        const isInt = v.tipo === 'internacional';
        L.circleMarker([v.lat, v.lon], {
          radius: isInt ? 8 : 6.5,
          color: isInt ? '#fdb813' : '#D71920',
          fillColor: isInt ? '#ffffff' : '#ff3843',
          fillOpacity: 0.95,
          weight: 2
        }).bindPopup(`
          <div class="popup-viagem">
            <strong class="titulo">${esc(v.local)}</strong>
            <span class="pais">${esc(v.pais || 'Brasil')}</span>
            <div class="data">📅 ${esc(v.data)}</div>
            <p class="motivo">${esc(v.motivo || '')}</p>
            <a href="${esc(v.fonte_url)}" target="_blank" rel="noopener" class="link-fonte">Ver registro oficial →</a>
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
let filtroAnoEntrega = 'todos';

function renderEntregas() {
  const q = (buscaInput ? buscaInput.value : '').toLowerCase().trim();
  const lista = entregas.filter(e => {
    const matchAno = filtroAnoEntrega === 'todos' || (e.data || '').startsWith(filtroAnoEntrega);
    if (!matchAno) return false;
    if (!q) return true;
    return [e.titulo, e.area, e.uf, e.descricao || '', e.data || ''].join(' ').toLowerCase().includes(q);
  });

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
  }).join('') || '<p class="sub" style="grid-column: 1 / -1; text-align: center; padding: 2.5rem;">Nenhuma entrega encontrada para este filtro ou busca.</p>';
}

const buscaInput = $('#busca-entregas');
if (buscaInput) {
  buscaInput.addEventListener('input', () => renderEntregas());
}

document.querySelectorAll('.chip-entrega').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.chip-entrega').forEach(b => b.classList.remove('ativo'));
    btn.classList.add('ativo');
    filtroAnoEntrega = btn.dataset.filtro;
    renderEntregas();
  });
});

renderEntregas();

// 5. Novo PAC — Transparência Oficial
const pac = D.novopac;
if (pac) {
  const pacStatsEl = $('#pac-stats');
  if (pacStatsEl) {
    pacStatsEl.innerHTML = `
      <div class="pac-card-stat">
        <div class="valor">${esc(pac.investimento_total)}</div>
        <div class="rotulo">Investimento Previsto Total</div>
      </div>
      <div class="pac-card-stat">
        <div class="valor">${esc(pac.investimento_mandato_2023_2026)}</div>
        <div class="rotulo">Previsto até 2026 (Mandato)</div>
      </div>
      <div class="pac-card-stat">
        <div class="valor">${esc(pac.total_empreendimentos)}</div>
        <div class="rotulo">Obras e Empreendimentos Mapeados</div>
      </div>
      <div class="pac-card-stat">
        <div class="valor">${esc(pac.fontes_financiamento[0].valor)}</div>
        <div class="rotulo">Atração de Investimentos Privados</div>
      </div>
    `;
  }

  const pacFontesEl = $('#pac-fontes');
  if (pacFontesEl && pac.fontes_financiamento) {
    pacFontesEl.innerHTML = pac.fontes_financiamento.map(f => `
      <div class="pac-fonte-item">
        <div class="pac-fonte-info">
          <strong>${esc(f.fonte)}</strong>
          <span>${esc(f.valor)} (${f.percentual}%)</span>
        </div>
        <div class="pac-barra-trilho">
          <div class="pac-barra-progresso" style="width: ${f.percentual}%"></div>
        </div>
      </div>
    `).join('');
  }
}
