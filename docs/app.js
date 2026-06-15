const money = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 });

let portfolio = {};
let strategies = [];
let paperPositions = [];
let paperTrades = [];
let paperPnlLedger = [];
let factors = [];
let proxies = [];
let navSeries = [];
let backtestNavSeries = [];
let market = [];
let news = [];
let macroRegime = {};
let strategyValidation = [];
let strategyCorrelation = {};

const $ = (id) => document.getElementById(id);
const pct = (v, d = 1) => `${Number(v).toFixed(d)}%`;
const cls = (v) => Number(v) < 0 ? "neg" : "pos";
const pill = (s) => `<span class="pill ${s}">${s}</span>`;
const dataBase = window.location.pathname.includes("/frontend/") ? "../data" : "./data";
const shortDate = (v) => v ? String(v).slice(0, 10) : "n/a";
const avg = (values) => values.length ? values.reduce((sum, v) => sum + v, 0) / values.length : 0;
const stdev = (values) => {
  if (values.length < 2) return 0;
  const m = avg(values);
  return Math.sqrt(values.reduce((sum, v) => sum + (v - m) ** 2, 0) / (values.length - 1));
};

async function loadJson(path) {
  const res = await fetch(path, { cache: "no-store" });
  if (!res.ok) throw new Error(`Failed to load ${path}`);
  return res.json();
}

async function loadOptionalJson(path, fallback) {
  try {
    return await loadJson(path);
  } catch (_err) {
    return fallback;
  }
}

async function loadData() {
  try {
    [portfolio, strategies, paperPositions, paperTrades, paperPnlLedger, factors, proxies, navSeries, backtestNavSeries, market, news, macroRegime, strategyValidation, strategyCorrelation] = await Promise.all([
      loadJson(`${dataBase}/portfolio.json`),
      loadJson(`${dataBase}/strategies.json`),
      loadOptionalJson(`${dataBase}/paper_positions.json`, []),
      loadOptionalJson(`${dataBase}/paper_trades.json`, []),
      loadOptionalJson(`${dataBase}/paper_pnl_ledger.json`, []),
      loadJson(`${dataBase}/factor_exposures.json`),
      loadJson(`${dataBase}/risk_proxies.json`),
      loadJson(`${dataBase}/nav_series.json`),
      loadJson(`${dataBase}/backtest_nav_series.json`),
      loadJson(`${dataBase}/market.json`),
      loadJson(`${dataBase}/market_news.json`),
      loadJson(`${dataBase}/macro_regime.json`),
      loadJson(`${dataBase}/strategy_validation.json`),
      loadJson(`${dataBase}/strategy_correlation.json`),
    ]);
  } catch (err) {
    const d = window.DASHBOARD_DATA;
    if (!d) throw err;
    portfolio = d.portfolio;
    strategies = d.strategies;
    paperPositions = d.paperPositions || [];
    paperTrades = d.paperTrades || [];
    paperPnlLedger = d.paperPnlLedger || [];
    factors = d.factorExposures;
    proxies = d.riskProxies;
    navSeries = d.navSeries;
    backtestNavSeries = d.backtestNavSeries || d.navSeries;
    market = d.market;
    news = d.marketNews;
    macroRegime = d.macroRegime || {};
    strategyValidation = d.strategyValidation || [];
    strategyCorrelation = d.strategyCorrelation || {};
  }
}

function table(id, headers, rows) {
  $(id).innerHTML = `
    <thead><tr>${headers.map((h) => `<th>${h}</th>`).join("")}</tr></thead>
    <tbody>${rows.map((r) => `<tr>${r.map((c) => `<td>${c}</td>`).join("")}</tr>`).join("")}</tbody>
  `;
}

function decisionReason(s) {
  if (s.action === "Pause") return "Signal quality is weak while drawdown or Sharpe breaches risk limits.";
  if (s.action === "Hedge") return "Macro or volatility exposure should be offset before adding risk.";
  if (s.action === "Reduce") return "Risk-adjusted performance, drawdown, or cost drag argues for smaller weight.";
  if (s.action === "Rebalance") return "Weight drift or warning status deserves review before trading.";
  if (s.action === "Increase") return "Sharpe and drawdown are acceptable; review capacity before increasing.";
  return "No immediate action; continue monitoring signal stability and exposure overlap.";
}

function renderPulse() {
  const paperWindowLabel = `${shortDate(portfolio.paperStart)} to ${shortDate(portfolio.paperEnd || portfolio.backtestEnd)}`;
  const paperWindow = $("paperWindow");
  if (paperWindow) paperWindow.textContent = paperWindowLabel;
  const cards = [
    ["Paper NAV", money.format(portfolio.nav), `${money.format(portfolio.inceptionPnl)} since paper start`, cls(portfolio.inceptionPnl)],
    ["Latest Day PnL", money.format(portfolio.dailyPnl), `Last close-to-close paper day: ${shortDate(portfolio.paperEnd || portfolio.backtestEnd)}`, cls(portfolio.dailyPnl)],
    ["Sharpe", Number(portfolio.sharpe).toFixed(2), "Use with drawdown and cost controls", "warn"],
    ["Drawdown", pct(portfolio.drawdown, 2), "Since paper start", "warn"],
    ["VaR / ES", `${money.format(portfolio.var95)} / ${money.format(portfolio.es95)}`, "95% tail risk estimate", "warn"],
    ["Turnover", pct(portfolio.turnover, 1), "Rebalance discipline input", "info"],
    ["Cost drag", `${Number(portfolio.costDragBps).toFixed(2)} bps`, "5 bps buy, 5 bps sell", "pos"],
    ["Universe", `${portfolio.universeSize || "n/a"} stocks`, portfolio.universeName || "Shared stock universe", "info"],
    ["Macro regime", macroRegime.riskTone || portfolio.regime || "Monitor", macroRegime.quadrant || "Growth / inflation overlay", "info"],
  ];
  $("pulseGrid").innerHTML = cards.map(([label, value, note, color]) => `
    <article class="pulse-card"><span>${label}</span><strong class="${color}">${value}</strong><small>${note}</small></article>
  `).join("");
}

function renderBacktestSummary() {
  const initial = Number(portfolio.initialCapital || 1000000);
  const fullNav = Number(portfolio.fullBacktestNav || (backtestNavSeries.length ? backtestNavSeries.at(-1) : portfolio.nav));
  const fullPnl = Number(portfolio.fullBacktestPnl ?? (fullNav - initial));
  const fullReturn = initial ? (fullNav / initial - 1) * 100 : 0;
  const cards = [
    ["Backtest Window", `${shortDate(portfolio.backtestStart)} to ${shortDate(portfolio.backtestEnd)}`, "Full historical research period", "info"],
    ["Full NAV", money.format(fullNav), `${money.format(fullPnl)} full-period PnL`, cls(fullPnl)],
    ["Full Return", pct(fullReturn, 1), "Net of modeled trading costs", cls(fullReturn)],
    ["Full Sharpe", Number(portfolio.fullBacktestSharpe ?? portfolio.sharpe).toFixed(2), "Historical risk-adjusted return", "warn"],
    ["Full Max DD", pct(portfolio.fullBacktestDrawdown ?? portfolio.drawdown, 2), "Worst peak-to-trough backtest loss", "warn"],
    ["Paper Start", shortDate(portfolio.paperStart), "Cockpit uses paper-window metrics", "info"],
  ];
  const el = $("backtestSummary");
  if (el) {
    el.innerHTML = cards.map(([label, value, note, color]) => `
      <article class="pulse-card"><span>${label}</span><strong class="${color}">${value}</strong><small>${note}</small></article>
    `).join("");
  }
}

function renderBacktestDiagnostics() {
  const nav = backtestNavSeries.map(Number).filter((value) => Number.isFinite(value));
  const target = $("backtestDiagnosticsTable");
  if (!target || nav.length < 2) return;

  const pnls = nav.slice(1).map((value, idx) => value - nav[idx]);
  const returns = nav.slice(1).map((value, idx) => nav[idx] ? value / nav[idx] - 1 : 0);
  const positiveRate = pnls.filter((value) => value > 0).length / pnls.length * 100;
  const bestPnl = Math.max(...pnls);
  const worstPnl = Math.min(...pnls);
  const avgPnl = avg(pnls);
  const annualVol = stdev(returns) * Math.sqrt(252) * 100;
  const totalReturn = nav[0] ? (nav.at(-1) / nav[0] - 1) * 100 : 0;

  const rows = [
    ["Trading days", pnls.length.toLocaleString(), "Completed close-to-close observations"],
    ["Positive days", pct(positiveRate, 1), "Share of days with positive portfolio PnL"],
    ["Best day", `<span class="pos">${money.format(bestPnl)}</span>`, "Largest one-day modeled gain"],
    ["Worst day", `<span class="neg">${money.format(worstPnl)}</span>`, "Largest one-day modeled loss"],
    ["Avg daily PnL", money.format(avgPnl), "Mean daily net PnL over full backtest"],
    ["Annualized vol", pct(annualVol, 1), "Volatility of daily portfolio returns"],
    ["Total return", pct(totalReturn, 1), "Full-period return after modeled costs"],
  ];
  table("backtestDiagnosticsTable", ["Metric", "Value", "Interpretation"], rows);
}

function renderDecisions() {
  const filter = $("actionFilter")?.value || "all";
  const score = { Breach: 3, Warning: 2, Healthy: 1 };
  const color = { Pause: "var(--red)", Reduce: "var(--red)", Hedge: "var(--amber)", Rebalance: "var(--blue)", Increase: "var(--green)" };
  const rows = strategies
    .filter((s) => s.action !== "Hold")
    .filter((s) => filter === "all" || s.action === filter)
    .sort((a, b) => (score[b.status] - score[a.status]) || (a.sharpe - b.sharpe))
    .slice(0, 7);
  $("decisionStack").innerHTML = rows.map((s) => `
    <article class="decision" style="border-left-color:${color[s.action] || "var(--aqua)"}">
      <div class="decision-head"><h3>${s.name}</h3><strong>${s.action}</strong></div>
      <p>${decisionReason(s)}</p>
      <p><b>${s.status}</b> · ${s.riskWindowDays || 126}D Sharpe ${Number(s.sharpe).toFixed(2)} · ${s.riskWindowDays || 126}D DD ${pct(s.drawdown)} · cost ${Number(s.costBps).toFixed(2)} bps</p>
    </article>
  `).join("");
}

function factorRow(f) {
  const ratio = Math.min(1, Math.abs(f.value / f.limit));
  const color = f.status === "Breach" ? "var(--red)" : f.status === "Warning" ? "var(--amber)" : "var(--green)";
  return `<div class="pressure-row"><span>${f.name}</span><div class="bar"><i style="width:${Math.max(5, ratio * 100)}%;background:${color}"></i></div><strong style="color:${color}">${Number(f.value).toFixed(3)}</strong></div>`;
}

function renderFactors() {
  $("factorPressure").innerHTML = factors.slice(0, 7).map(factorRow).join("");
  $("factorTable").innerHTML = factors.map(factorRow).join("");
}

function renderWatchlist() {
  const rows = strategies.filter((s) => s.status !== "Healthy" || s.action !== "Hold").slice(0, 9).map((s) => [
    `<strong>${s.name}</strong>`,
    s.action,
    pct(s.weight),
    `<span class="${cls(s.pnl)}">${money.format(s.pnl)}</span>`,
    Number(s.sharpe).toFixed(2),
    pct(s.drawdown),
    `${s.signal}/100`,
    pill(s.status),
  ]);
  table("watchlistTable", ["Strategy", "Action", "Weight", "Daily PnL", "126D Sharpe", "126D DD", "Signal", "Status"], rows);
}

function renderCorrelationPlot() {
  const labels = (strategyCorrelation.labels || []).slice(0, 10);
  const names = (strategyCorrelation.names || []).slice(0, 10);
  const matrix = strategyCorrelation.matrix || [];
  if (!labels.length || !matrix.length) return;
  $("corrMeta").textContent = `Rolling ${strategyCorrelation.actualWindowDays || strategyCorrelation.windowDays}D · ${strategyCorrelation.timing} · as of ${strategyCorrelation.asOf}`;
  const cellColor = (v) => v > 0.75 ? "var(--red)" : v > 0.55 ? "var(--amber)" : v > 0.25 ? "var(--blue)" : "var(--green)";
  let html = `<div class="corr-label"></div>`;
  html += labels.map((id) => `<div class="corr-label">${id.replace("STR-", "S")}</div>`).join("");
  labels.forEach((rowId, i) => {
    html += `<div class="corr-label">${rowId.replace("STR-", "S")}</div>`;
    labels.forEach((colId, j) => {
      const v = Number(matrix[i][j] || 0);
      html += `<div class="corr-cell" title="${names[i]} vs ${names[j]}: ${v.toFixed(2)}" style="background:${cellColor(v)};opacity:${0.28 + Math.abs(v) * 0.72}">${i === j ? "1.00" : ""}</div>`;
    });
  });
  $("corrPlot").innerHTML = html;
}

function renderHotspots() {
  const pairs = strategyCorrelation.highCorrelationPairs || [];
  if (!pairs.length) {
    $("hotspots").innerHTML = `<div class="hotspot"><div><b>No high-correlation pairs</b><br><span>Rolling correlation remains below warning threshold.</span></div><strong>OK</strong></div>`;
    return;
  }
  $("hotspots").innerHTML = pairs.slice(0, 4).map((p) => `
    <div class="hotspot">
      <div><b>${p.leftId} / ${p.rightId}</b><br><span>${p.leftName} vs ${p.rightName}</span></div>
      <strong>${Number(p.correlation).toFixed(2)}</strong>
    </div>
  `).join("");
}

function renderStrategyBook() {
  const q = ($("strategySearch")?.value || "").toLowerCase();
  const rows = strategies
    .filter((s) => `${s.name} ${s.sleeve}`.toLowerCase().includes(q))
    .map((s) => [
      `<strong>${s.id}</strong>`,
      `<strong>${s.name}</strong><br><span>${s.sleeve}</span>`,
      s.holdings,
      pct(s.targetWeight),
      pct(s.weight),
      `<span class="${Math.abs(s.weight - s.targetWeight) > 0.5 ? "warn" : "pos"}">${pct(s.weight - s.targetWeight)}</span>`,
      money.format(s.capital),
      `<span class="${cls(s.pnl)}">${money.format(s.pnl)}</span>`,
      Number(s.sharpe).toFixed(2),
      pct(s.drawdown),
      `${Number(s.costBps).toFixed(2)} bps`,
      s.engine || "placeholder",
      s.action,
      pill(s.status),
    ]);
  table("strategyTable", ["ID", "Strategy", "Latest Top Holdings", "Target", "Current", "Drift", "Capital", "Daily PnL", "126D Sharpe", "126D DD", "Cost", "Engine", "Decision", "Status"], rows);
}

function renderPaperLedger() {
  const latestPositionDate = paperPositions.length ? paperPositions.at(-1).date : "";
  const positionRows = paperPositions
    .filter((row) => row.date === latestPositionDate)
    .slice(0, 30)
    .map((row) => [
      row.date,
      row.strategyId,
      row.ticker,
      pct(Number(row.weight) * 100, 1),
      money.format(row.notional),
    ]);
  table("paperPositionsTable", ["Date", "Strategy", "Ticker", "Stock Weight", "Notional"], positionRows);

  const tradeRows = [...paperTrades]
    .slice(-40)
    .reverse()
    .map((row) => [
      row.date,
      row.strategyId,
      row.ticker,
      `<span class="${row.side === "BUY" ? "pos" : "neg"}">${row.side}</span>`,
      pct(Number(row.weightChange) * 100, 1),
      money.format(row.notional),
      money.format(row.cost),
    ]);
  table("paperTradesTable", ["Date", "Strategy", "Ticker", "Side", "Weight Change", "Notional", "Cost"], tradeRows);

  const pnlRows = [...paperPnlLedger]
    .slice(-40)
    .reverse()
    .map((row) => [
      row.date,
      row.strategyId,
      `<span class="${cls(row.grossPnl)}">${money.format(row.grossPnl)}</span>`,
      money.format(row.cost),
      `<span class="${cls(row.netPnl)}">${money.format(row.netPnl)}</span>`,
      money.format(row.navAfter),
      pct(row.turnover, 1),
    ]);
  table("paperPnlTable", ["Date", "Strategy", "Gross PnL", "Cost", "Net PnL", "Strategy NAV", "Turnover"], pnlRows);
}

function renderProxyTable() {
  const rows = proxies.map((p) => [
    `<strong>${p.ticker}</strong>`, p.factor, p.purpose,
    `<span class="${p.loading < 0 ? "neg" : "pos"}">${Number(p.loading).toFixed(3)}</span>`,
    p.use,
  ]);
  table("proxyTable", ["ETF Proxy", "Risk Factor", "Purpose", "Portfolio Loading", "Use In Dashboard"], rows);
}

function renderRiskContribution() {
  const items = [...strategies].sort((a, b) => Math.abs(b.weight * b.drawdown) - Math.abs(a.weight * a.drawdown)).slice(0, 9);
  $("riskContribution").innerHTML = items.map((s) => {
    const raw = Math.abs(s.weight * s.drawdown);
    return `<div class="pressure-row"><span>${s.name}</span><div class="bar"><i style="width:${Math.min(100, raw)}%;background:var(--violet)"></i></div><strong class="violet">${(raw / 10).toFixed(1)}%</strong></div>`;
  }).join("");
  const rows = strategies.filter((s) => s.status !== "Healthy").map((s) => [
    `<strong>${s.name}</strong>`,
    s.sharpe < 0 ? "126D Sharpe" : "126D Drawdown",
    s.sharpe < 0 ? Number(s.sharpe).toFixed(2) : pct(s.drawdown),
    s.sharpe < 0 ? "-0.50 minimum" : "-8.00%",
    s.action,
    pill(s.status),
  ]);
  table("limitTable", ["Strategy", "Control", "Current", "Threshold", "Action", "Status"], rows);
}

function renderMarket() {
  $("marketTiles").innerHTML = market.map((m) => `<article class="market-tile"><span>${m.asset}</span><strong>${m.state}</strong><p><b>${m.value}</b> · ${m.note}</p></article>`).join("");
}

function renderMacroRegime() {
  if (!macroRegime || !macroRegime.quadrant) return;
  $("macroSource").textContent = macroRegime.source || "Macro source";
  const quadrants = [
    ["Rising growth + rising inflation", "Inflationary expansion"],
    ["Rising growth + falling inflation", "Goldilocks / risk-on"],
    ["Falling growth + rising inflation", "Stagflation risk"],
    ["Falling growth + falling inflation", "Defensive slowdown"],
  ];
  $("regimeQuadrant").innerHTML = `
    <article class="regime-summary">
      <span>Current regime</span>
      <strong>${macroRegime.quadrant}</strong>
      <p>${macroRegime.riskTone} · ${macroRegime.businessCycle}</p>
    </article>
    <div class="quadrant-grid">
      ${quadrants.map(([name, note]) => `<div class="quadrant ${name === macroRegime.quadrant ? "active" : ""}"><b>${name}</b><span>${note}</span></div>`).join("")}
    </div>
    <div class="macro-warning">${(macroRegime.warnings || []).map((w) => `<p>${w}</p>`).join("")}</div>
  `;
  $("macroIndicators").innerHTML = `
    <div class="macro-score"><span>Growth</span><strong class="${macroRegime.growth.direction === "Rising" ? "pos" : "neg"}">${macroRegime.growth.direction}</strong><small>${Number(macroRegime.growth.score).toFixed(3)}</small></div>
    <div class="macro-score"><span>Inflation</span><strong class="${macroRegime.inflation.direction === "Rising" ? "warn" : "pos"}">${macroRegime.inflation.direction}</strong><small>${Number(macroRegime.inflation.score).toFixed(3)}</small></div>
    <div class="macro-score"><span>Stress</span><strong class="${macroRegime.stress.direction === "Rising" ? "neg" : "pos"}">${macroRegime.stress.direction}</strong><small>${Number(macroRegime.stress.score).toFixed(3)}</small></div>
    <div class="indicator-list">${(macroRegime.indicators || []).map((i) => `<div><span>${i.name}</span><b>${i.value}</b></div>`).join("")}</div>
  `;
  $("regimeGuidance").innerHTML = (macroRegime.guidance || []).map((g) => `
    <article class="guidance-card">
      <div><span>${g.sleeve}</span><strong>${g.tilt}</strong></div>
      <p>${g.reason}</p>
    </article>
  `).join("");
}

function renderNewsFeed() {
  $("newsFeed").innerHTML = news.map((n) => `<article class="news-item"><header><b>${n.time}</b><span>${n.impact} relevance</span></header><p>${n.headline}</p><p><span>${n.source}</span> · ${n.tickers}</p></article>`).join("");
}

function renderStress() {
  const rows = [
    ["COVID shock", "-8.9%", "-12.4%", "Healthy", "Lower equity beta helps relative drawdown"],
    ["2022 inflation/rates", "-11.7%", "-16.8%", "Warning", "Momentum and duration-sensitive growth need review"],
    ["Credit spread shock", "-6.4%", "-9.2%", "Breach", "Credit-sensitive stock baskets should reduce faster"],
    ["Volatility spike", "-5.8%", "-8.1%", "Warning", "Range and volatility alphas need hedge review"],
  ];
  table("stressTable", ["Stress period", "Portfolio DD", "Benchmark DD", "Status", "Finding"], rows.map((r) => [r[0], r[1], r[2], pill(r[3]), r[4]]));
}

function renderValidation() {
  const first = strategyValidation[0] || {};
  const split = $("validationSplit");
  if (split) {
    split.textContent = `Research period: ${shortDate(first.inSampleStart)} to ${shortDate(first.inSampleEnd)} · OOS validation: ${shortDate(first.outOfSampleStart)} to ${shortDate(first.outOfSampleEnd)}`;
  }
  const rows = strategyValidation.map((s) => [
    `<strong>${s.id}</strong>`,
    `<strong>${s.name}</strong><br><span>${s.sleeve}</span>`,
    Number(s.inSampleSharpe).toFixed(2),
    Number(s.outOfSampleSharpe).toFixed(2),
    `<span class="${cls(s.sharpeDecay)}">${Number(s.sharpeDecay).toFixed(2)}</span>`,
    pct(s.inSampleDrawdown, 1),
    pct(s.outOfSampleDrawdown, 1),
    pct(s.outOfSampleHitRate, 1),
    pct(s.outOfSampleReturn, 1),
    `<strong>${s.oosValidationStatus}</strong><br><span>${s.oosValidationReason}</span>`,
  ]);
  table("validationTable", ["ID", "Strategy", "IS Sharpe", "OOS Sharpe", "Decay", "IS DD", "OOS DD", "OOS Hit", "OOS Return", "Validation"], rows);
}

function renderWorkflow() {
  const rows = strategies.slice(0, 12).map((s, i) => [
    `<strong>${s.name}</strong>`, "Done", "Done", i % 4 === 0 ? "Review" : "Done", i % 5 === 0 ? "Review" : "Done",
    i % 3 === 0 ? "In progress" : "Done", s.status, "Live-style", s.action,
  ]);
  table("workflowTable", ["Strategy", "Idea", "Hypothesis", "Data", "Signal", "Backtest", "Risk limits", "Monitoring", "Allocation"], rows);
}

function drawChart(id, values, color) {
  const canvas = $(id);
  if (!canvas || !values.length) return;
  const ctx = canvas.getContext("2d");
  const rect = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  const h = Number(canvas.dataset.height || canvas.getAttribute("height") || 250);
  canvas.dataset.height = String(h);
  canvas.style.height = `${h}px`;
  canvas.width = Math.floor(rect.width * dpr);
  canvas.height = Math.floor(h * dpr);
  ctx.scale(dpr, dpr);
  ctx.clearRect(0, 0, rect.width, h);
  ctx.strokeStyle = "#22303d";
  ctx.lineWidth = 1;
  for (let i = 1; i < 4; i++) { const y = (h / 4) * i; ctx.beginPath(); ctx.moveTo(18, y); ctx.lineTo(rect.width - 18, y); ctx.stroke(); }
  const min = Math.min(...values), max = Math.max(...values), pad = Math.max(1, (max - min) * 0.12);
  const x = (i) => 18 + (i / (values.length - 1)) * (rect.width - 36);
  const y = (v) => h - 20 - ((v - min + pad) / (max - min + pad * 2)) * (h - 42);
  ctx.beginPath();
  values.forEach((v, i) => i ? ctx.lineTo(x(i), y(v)) : ctx.moveTo(x(i), y(v)));
  ctx.strokeStyle = color; ctx.lineWidth = 3; ctx.stroke();
  ctx.lineTo(rect.width - 18, h - 20); ctx.lineTo(18, h - 20); ctx.closePath();
  ctx.fillStyle = color === "#f47a67" ? "rgba(244,122,103,.10)" : "rgba(97,215,194,.10)";
  ctx.fill();
}

function renderCharts() {
  const metric = $("chartMetric")?.value || "nav";
  let values = navSeries;
  let color = "#61d7c2";
  if (metric === "drawdown") {
    let peak = navSeries[0];
    values = navSeries.map((v) => { peak = Math.max(peak, v); return ((v / peak) - 1) * 100; });
    color = "#f47a67";
  }
  if (metric === "pnl") {
    values = navSeries.map((v, i) => i === 0 ? 0 : v - navSeries[i - 1]);
    color = "#7aa7ff";
  }
  drawChart("navChart", values, color);
  drawChart("backtestChart", backtestNavSeries, "#7aa7ff");
}

function setView(view) {
  document.querySelectorAll(".view").forEach((el) => el.classList.remove("active"));
  document.querySelectorAll(".mode").forEach((el) => el.classList.remove("active"));
  $(`view-${view}`).classList.add("active");
  document.querySelector(`[data-view="${view}"]`).classList.add("active");
  setTimeout(renderCharts, 30);
}

function renderAll() {
  renderPulse(); renderBacktestSummary(); renderDecisions(); renderFactors(); renderWatchlist(); renderHotspots(); renderCorrelationPlot();
  renderStrategyBook(); renderPaperLedger(); renderProxyTable(); renderRiskContribution(); renderBacktestDiagnostics(); renderMarket(); renderMacroRegime(); renderNewsFeed(); renderStress(); renderValidation(); renderWorkflow(); renderCharts();
}

document.addEventListener("DOMContentLoaded", async () => {
  await loadData();
  renderAll();
  document.querySelector(".modebar").addEventListener("click", (event) => {
    const mode = event.target.closest("[data-view]");
    if (mode) setView(mode.dataset.view);
  });
  $("actionFilter").addEventListener("change", renderDecisions);
  $("strategySearch").addEventListener("input", renderStrategyBook);
  $("chartMetric").addEventListener("change", renderCharts);
  $("refreshBtn").addEventListener("click", () => window.location.reload());
  window.addEventListener("resize", renderCharts);
});
