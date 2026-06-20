/**
 * =============================================================================
 * Customer Value Intelligence — Dashboard Interactivity
 * =============================================================================
 * Renders all four panels + segment cards + ICP from embedded data.
 * No external dependencies — pure vanilla JS.
 * =============================================================================
 */

// ─────────────────────────────────────────────────────────────────────────────
// DATA (embedded from SQL query results)
// ─────────────────────────────────────────────────────────────────────────────

const DATA = {
  pyramid: [
    { tier: "Platinum", customers: 972, revenue: 2636036, revenuePct: 65.1, customerPct: 24.9 },
    { tier: "Gold",     customers: 969, revenue: 1002232, revenuePct: 24.7, customerPct: 24.8 },
    { tier: "Silver",   customers: 978, revenue: 325098,  revenuePct: 8.0,  customerPct: 25.1 },
    { tier: "Bronze",   customers: 981, revenue: 88463,   revenuePct: 2.2,  customerPct: 25.2 },
  ],

  segments: [
    {
      name: "Champions", key: "champions", count: 758, pct: 19.4,
      revenuePct: 42.2, avgSpend: 2257, avgAge: 44.7, avgPrev: 33.5,
      avgFreq: 37.5, loyalty: 0.6575, promoPct: 56.3, promoDep: 0.0564,
      subPct: 45.6, rating: 4.11, satPct: 70.8
    },
    {
      name: "At-Risk", key: "at-risk", count: 1031, pct: 26.4,
      revenuePct: 31.0, avgSpend: 1217, avgAge: 44.8, avgPrev: 32.7,
      avgFreq: 20.3, loyalty: 0.3777, promoPct: 42.2, promoDep: 0.0807,
      subPct: 25.0, rating: 3.22, satPct: 0.0
    },
    {
      name: "Casual Browsers", key: "casual", count: 1454, pct: 37.3,
      revenuePct: 21.0, avgSpend: 584, avgAge: 43.5, avgPrev: 17.5,
      avgFreq: 9.8, loyalty: 0.2888, promoPct: 15.6, promoDep: 0.077,
      subPct: 6.7, rating: 3.91, satPct: 54.3
    },
    {
      name: "Discount Hunters", key: "discount", count: 436, pct: 11.2,
      revenuePct: 4.4, avgSpend: 405, avgAge: 43.5, avgPrev: 12.2,
      avgFreq: 6.9, loyalty: 0.2344, promoPct: 100.0, promoDep: 0.6723,
      subPct: 49.8, rating: 3.52, satPct: 22.5
    },
    {
      name: "Loyal Regulars", key: "loyal", count: 221, pct: 5.7,
      revenuePct: 1.5, avgSpend: 271, avgAge: 43.3, avgPrev: 40.2,
      avgFreq: 6.5, loyalty: 0.5928, promoPct: 68.8, promoDep: 0.1549,
      subPct: 60.6, rating: 4.39, satPct: 95.0
    },
  ],

  geoHiddenGems: [
    { state: "Illinois",   region: "Midwest",   count: 92, avgSpend: 1269, promoPct: 40.2, promoDep: 0.1134 },
    { state: "Alaska",     region: "West",       count: 72, avgSpend: 1263, promoPct: 40.3, promoDep: 0.1203 },
    { state: "Tennessee",  region: "South",      count: 77, avgSpend: 1258, promoPct: 36.4, promoDep: 0.1275 },
    { state: "Louisiana",  region: "South",      count: 84, avgSpend: 1245, promoPct: 41.7, promoDep: 0.1211 },
    { state: "Georgia",    region: "South",      count: 79, avgSpend: 1212, promoPct: 40.5, promoDep: 0.1311 },
    { state: "New York",   region: "Northeast",  count: 87, avgSpend: 1159, promoPct: 41.4, promoDep: 0.1591 },
    { state: "Alabama",    region: "South",      count: 89, avgSpend: 1121, promoPct: 40.4, promoDep: 0.1505 },
    { state: "Wyoming",    region: "West",       count: 71, avgSpend: 1112, promoPct: 42.3, promoDep: 0.1260 },
    { state: "Arizona",    region: "West",       count: 65, avgSpend: 1108, promoPct: 33.8, promoDep: 0.1156 },
    { state: "Virginia",   region: "South",      count: 77, avgSpend: 1107, promoPct: 37.7, promoDep: 0.1314 },
    { state: "Rhode Island", region: "Northeast", count: 63, avgSpend: 1068, promoPct: 39.7, promoDep: 0.1499 },
    { state: "Nebraska",   region: "Midwest",    count: 87, avgSpend: 1053, promoPct: 42.5, promoDep: 0.1547 },
    { state: "Texas",      region: "South",      count: 77, avgSpend: 1041, promoPct: 36.4, promoDep: 0.1283 },
  ],

  categoryFunnel: [
    { category: "Outerwear",   count: 324,  avgPrev: 25.6, avgSpend: 1052, promoPct: 43.2, newCust: 64,  vetCust: 74 },
    { category: "Footwear",    count: 599,  avgPrev: 25.3, avgSpend: 1034, promoPct: 43.6, newCust: 119, vetCust: 122 },
    { category: "Clothing",    count: 1737, avgPrev: 25.3, avgSpend: 1043, promoPct: 42.5, newCust: 352, vetCust: 390 },
    { category: "Accessories", count: 1240, avgPrev: 25.7, avgSpend: 1045, promoPct: 43.8, newCust: 242, vetCust: 285 },
  ],

  icp: {
    avgAge: 44.7, minAge: 18, maxAge: 70,
    avgPurchase: 61.5, avgAnnualSpend: 2257,
    avgPrev: 33.5, avgFreq: 37.5,
    avgRating: 4.11, promoPct: 56.3, subPct: 45.6,
    count: 758,
    dominantGender: "Male (76%)",
    topAgeGroup: "46-55",
    topCategory: "Clothing (45%)",
    topPayment: "Credit Card",
  },

  revenueConcentration: [
    { segment: "Champions",       promo: 919272,  organic: 791706 },
    { segment: "At-Risk",         promo: 446203,  organic: 808574 },
    { segment: "Casual Browsers", promo: 151760,  organic: 697718 },
    { segment: "Discount Hunters", promo: 176757, organic: 0 },
    { segment: "Loyal Regulars",  promo: 42042,   organic: 17797 },
  ],
};

// ─────────────────────────────────────────────────────────────────────────────
// UTILITY FUNCTIONS
// ─────────────────────────────────────────────────────────────────────────────

function $(selector) { return document.querySelector(selector); }
function $$(selector) { return document.querySelectorAll(selector); }

function formatCurrency(num) {
  if (num >= 1000000) return `$${(num / 1000000).toFixed(2)}M`;
  if (num >= 1000) return `$${(num / 1000).toFixed(1)}K`;
  return `$${num.toLocaleString()}`;
}

function formatNumber(num) {
  return num.toLocaleString();
}

function createElement(tag, className, innerHTML) {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (innerHTML) el.innerHTML = innerHTML;
  return el;
}

// ─────────────────────────────────────────────────────────────────────────────
// PANEL 1: CUSTOMER VALUE PYRAMID
// ─────────────────────────────────────────────────────────────────────────────

function renderPyramid() {
  const container = $("#pyramid-chart");
  const maxRevenue = Math.max(...DATA.pyramid.map(d => d.revenuePct));

  DATA.pyramid.forEach((tier, i) => {
    const barWidth = Math.max(15, (tier.revenuePct / maxRevenue) * 100);
    const tierClass = tier.tier.toLowerCase();

    const row = createElement("div", "pyramid-tier");
    row.innerHTML = `
      <div class="tier-label" style="color: var(--color-${tierClass})">${tier.tier}</div>
      <div class="tier-bar-container">
        <div class="tier-bar ${tierClass}" style="width: 0%; transition-delay: ${i * 150}ms">
          <div class="tier-bar-inner">
            <span class="tier-customers">${formatNumber(tier.customers)} customers</span>
            <span class="tier-revenue">${tier.revenuePct}% revenue</span>
          </div>
        </div>
      </div>
    `;
    container.appendChild(row);

    // Animate bar width
    requestAnimationFrame(() => {
      setTimeout(() => {
        row.querySelector(".tier-bar").style.width = `${barWidth}%`;
      }, 300 + i * 150);
    });
  });

  // Legend
  const legend = createElement("div", "pyramid-legend");
  legend.innerHTML = `
    <div class="legend-item">
      <div class="legend-dot" style="background: var(--color-platinum)"></div>
      <span>Bar width = share of total revenue</span>
    </div>
    <div class="legend-item">
      <div class="legend-dot" style="background: var(--accent-emerald)"></div>
      <span>Top 25% of customers = 65% of revenue</span>
    </div>
  `;
  container.appendChild(legend);
}

// ─────────────────────────────────────────────────────────────────────────────
// PANEL 2: PROMO DEPENDENCY vs LOYALTY (SCATTER)
// ─────────────────────────────────────────────────────────────────────────────

function renderScatter() {
  const axes = $("#scatter-axes");
  const rect = axes.getBoundingClientRect();
  const w = rect.width || 500;
  const h = rect.height || 320;

  // Segment colors
  const colors = {
    "Champions": "var(--color-champions)",
    "Loyal Regulars": "var(--color-loyal)",
    "At-Risk": "var(--color-at-risk)",
    "Discount Hunters": "var(--color-discount)",
    "Casual Browsers": "var(--color-casual)",
  };

  // Data points (segments)
  const points = DATA.segments.map(s => ({
    x: s.promoDep,
    y: s.loyalty,
    name: s.name,
    size: Math.sqrt(s.count) * 2.2,
    color: colors[s.name],
    count: s.count,
    spend: s.avgSpend,
    promoPct: s.promoPct,
  }));

  // Scale
  const xMax = 0.8;
  const yMax = 0.75;
  const xScale = (v) => (v / xMax) * 100;
  const yScale = (v) => (1 - v / yMax) * 100;

  // Grid lines
  for (let i = 0.1; i <= 0.7; i += 0.1) {
    const hLine = createElement("div", "scatter-grid-line horizontal");
    hLine.style.top = `${yScale(i)}%`;
    axes.appendChild(hLine);

    const tick = createElement("div", "scatter-tick");
    tick.style.top = `${yScale(i)}%`;
    tick.style.left = "-40px";
    tick.style.transform = "translateY(-50%)";
    tick.textContent = i.toFixed(1);
    axes.appendChild(tick);
  }

  for (let i = 0.1; i <= 0.7; i += 0.1) {
    const vLine = createElement("div", "scatter-grid-line vertical");
    vLine.style.left = `${xScale(i)}%`;
    axes.appendChild(vLine);

    const tick = createElement("div", "scatter-tick");
    tick.style.bottom = "-20px";
    tick.style.left = `${xScale(i)}%`;
    tick.style.transform = "translateX(-50%)";
    tick.textContent = i.toFixed(1);
    axes.appendChild(tick);
  }

  // Quadrant labels
  const quadrants = [
    { text: "LOYAL & INDEPENDENT", x: "15%", y: "8%", color: "var(--accent-emerald)", opacity: 0.15 },
    { text: "LOYAL & PROMO-USING", x: "65%", y: "8%", color: "var(--accent-indigo)", opacity: 0.12 },
    { text: "DETACHED", x: "15%", y: "85%", color: "var(--accent-amber)", opacity: 0.12 },
    { text: "DISCOUNT-DEPENDENT", x: "65%", y: "85%", color: "var(--accent-rose)", opacity: 0.15 },
  ];
  quadrants.forEach(q => {
    const label = createElement("div", "");
    label.style.cssText = `
      position: absolute; left: ${q.x}; top: ${q.y};
      font-size: 0.55rem; font-weight: 700; letter-spacing: 0.1em;
      color: ${q.color}; opacity: ${q.opacity};
      text-transform: uppercase; pointer-events: none;
    `;
    label.textContent = q.text;
    axes.appendChild(label);
  });

  // Plot points
  points.forEach((p, i) => {
    const point = createElement("div", "scatter-point");
    const left = xScale(p.x);
    const top = yScale(p.y);

    point.style.cssText = `
      left: ${left}%; top: ${top}%;
      width: ${p.size}px; height: ${p.size}px;
      background: ${p.color};
      transform: translate(-50%, -50%) scale(0);
      transition: transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) ${i * 100 + 500}ms;
      box-shadow: 0 0 ${p.size}px ${p.color}40;
    `;

    point.innerHTML = `
      <span class="scatter-point-label">${p.name}</span>
      <div class="scatter-tooltip" style="bottom: calc(100% + 10px); left: 50%; transform: translateX(-50%);">
        <strong>${p.name}</strong><br>
        Customers: ${formatNumber(p.count)}<br>
        Avg Spend: ${formatCurrency(p.spend)}/yr<br>
        Promo Usage: ${p.promoPct}%<br>
        Loyalty: ${p.y.toFixed(3)}
      </div>
    `;

    axes.appendChild(point);

    requestAnimationFrame(() => {
      setTimeout(() => {
        point.style.transform = "translate(-50%, -50%) scale(1)";
      }, 100);
    });
  });
}

// ─────────────────────────────────────────────────────────────────────────────
// PANEL 3: GEOGRAPHIC OPPORTUNITY MAP
// ─────────────────────────────────────────────────────────────────────────────

function renderGeo() {
  const container = $("#geo-chart");
  const avgPromo = 43.0; // Overall average

  // Group by region
  const regions = {};
  DATA.geoHiddenGems.forEach(s => {
    if (!regions[s.region]) regions[s.region] = [];
    regions[s.region].push(s);
  });

  Object.entries(regions).sort((a, b) => {
    const avgA = a[1].reduce((sum, s) => sum + s.avgSpend, 0) / a[1].length;
    const avgB = b[1].reduce((sum, s) => sum + s.avgSpend, 0) / b[1].length;
    return avgB - avgA;
  }).forEach(([region, states]) => {
    const regionAvg = states.reduce((s, st) => s + st.avgSpend, 0) / states.length;

    const header = createElement("div", "geo-region-header");
    header.innerHTML = `
      <span>${region}</span>
      <span class="geo-region-stat">${states.length} hidden-gem states · Avg Spend: ${formatCurrency(regionAvg)}/yr</span>
    `;
    container.appendChild(header);

    const grid = createElement("div", "geo-grid");
    states.sort((a, b) => b.avgSpend - a.avgSpend).forEach(state => {
      const cardClass = state.promoPct < avgPromo - 5 ? "organic" : (state.promoPct > avgPromo ? "promo" : "mixed");
      const card = createElement("div", `geo-card ${cardClass}`);
      card.innerHTML = `
        <div class="geo-state">${state.state}</div>
        <div class="geo-metrics">
          <div class="geo-metric">
            <span>Avg Spend</span>
            <span class="geo-metric-value">${formatCurrency(state.avgSpend)}</span>
          </div>
          <div class="geo-metric">
            <span>Promo %</span>
            <span class="geo-metric-value">${state.promoPct}%</span>
          </div>
          <div class="geo-metric">
            <span>Customers</span>
            <span class="geo-metric-value">${state.count}</span>
          </div>
        </div>
      `;
      grid.appendChild(card);
    });
    container.appendChild(grid);
  });

  // Legend
  const legend = createElement("div", "geo-legend");
  legend.innerHTML = `
    <div class="geo-legend-item">
      <div class="geo-legend-bar" style="background: var(--accent-emerald)"></div>
      <span>Organic (promo &lt; 38%)</span>
    </div>
    <div class="geo-legend-item">
      <div class="geo-legend-bar" style="background: var(--accent-amber)"></div>
      <span>Mixed (38–43%)</span>
    </div>
    <div class="geo-legend-item">
      <div class="geo-legend-bar" style="background: var(--accent-rose)"></div>
      <span>Promo-leaning (&gt; 43%)</span>
    </div>
  `;
  container.appendChild(legend);
}

// ─────────────────────────────────────────────────────────────────────────────
// PANEL 4: CATEGORY RETENTION FUNNEL
// ─────────────────────────────────────────────────────────────────────────────

function renderFunnel() {
  const container = $("#funnel-chart");

  // Sort by avg previous purchases (ascending = entry point first)
  const sorted = [...DATA.categoryFunnel].sort((a, b) => a.avgPrev - b.avgPrev);

  sorted.forEach((cat, i) => {
    const newPct = (cat.newCust / cat.count * 100).toFixed(1);
    const vetPct = (cat.vetCust / cat.count * 100).toFixed(1);
    const midPct = (100 - parseFloat(newPct) - parseFloat(vetPct)).toFixed(1);

    const item = createElement("div", "funnel-item");
    item.innerHTML = `
      <div class="funnel-header">
        <div class="funnel-label">${cat.category}</div>
        <div class="funnel-value">${cat.count} customers · Avg ${cat.avgPrev} prev purchases · ${formatCurrency(cat.avgSpend)}/yr</div>
      </div>
      <div class="funnel-bar-track">
        <div class="funnel-bar-segments" style="opacity: 0; transition: opacity 0.6s ease ${i * 150 + 400}ms">
          <div class="funnel-bar-new" style="width: ${newPct}%">
            <span class="funnel-bar-text">${newPct}%</span>
          </div>
          <div class="funnel-bar-mid" style="width: ${midPct}%"></div>
          <div class="funnel-bar-veteran" style="width: ${vetPct}%">
            <span class="funnel-bar-text">${vetPct}%</span>
          </div>
        </div>
      </div>
      <div class="funnel-meta">
        <span><span class="dot new"></span> New (≤10 purchases): ${cat.newCust}</span>
        <span><span class="dot veteran"></span> Veteran (≥40 purchases): ${cat.vetCust}</span>
        <span>Promo Rate: ${cat.promoPct}%</span>
      </div>
    `;
    container.appendChild(item);

    // Animate
    requestAnimationFrame(() => {
      setTimeout(() => {
        item.querySelector(".funnel-bar-segments").style.opacity = "1";
      }, 100);
    });
  });

  // Legend
  const legend = createElement("div", "pyramid-legend");
  legend.innerHTML = `
    <div class="legend-item">
      <div class="legend-dot" style="background: var(--accent-rose)"></div>
      <span>New customers (entry point signal)</span>
    </div>
    <div class="legend-item">
      <div class="legend-dot" style="background: var(--accent-emerald)"></div>
      <span>Veterans (retention signal)</span>
    </div>
  `;
  container.appendChild(legend);
}

// ─────────────────────────────────────────────────────────────────────────────
// SEGMENT DETAIL CARDS
// ─────────────────────────────────────────────────────────────────────────────

function renderSegmentCards() {
  const container = $("#segment-cards");

  const cssClasses = {
    "Champions": "champions",
    "Loyal Regulars": "loyal",
    "At-Risk": "at-risk",
    "Discount Hunters": "discount",
    "Casual Browsers": "casual",
  };

  DATA.segments.forEach(seg => {
    const card = createElement("div", `segment-card ${cssClasses[seg.name]}`);
    card.innerHTML = `
      <div class="segment-name" style="color: var(--color-${cssClasses[seg.name]})">${seg.name}</div>
      <div class="segment-count">${formatNumber(seg.count)} customers (${seg.pct}%)</div>
      <div class="segment-metrics">
        <div class="segment-metric">
          <span class="segment-metric-label">Revenue Share</span>
          <span class="segment-metric-value">${seg.revenuePct}%</span>
        </div>
        <div class="segment-metric">
          <span class="segment-metric-label">Avg Annual Spend</span>
          <span class="segment-metric-value">${formatCurrency(seg.avgSpend)}</span>
        </div>
        <div class="segment-metric">
          <span class="segment-metric-label">Loyalty Score</span>
          <span class="segment-metric-value">${seg.loyalty.toFixed(3)}</span>
        </div>
        <div class="segment-metric">
          <span class="segment-metric-label">Promo Usage</span>
          <span class="segment-metric-value">${seg.promoPct}%</span>
        </div>
        <div class="segment-metric">
          <span class="segment-metric-label">Promo Dependency</span>
          <span class="segment-metric-value">${seg.promoDep.toFixed(3)}</span>
        </div>
        <div class="segment-metric">
          <span class="segment-metric-label">Subscription</span>
          <span class="segment-metric-value">${seg.subPct}%</span>
        </div>
        <div class="segment-metric">
          <span class="segment-metric-label">Avg Rating</span>
          <span class="segment-metric-value">${seg.rating}</span>
        </div>
        <div class="segment-metric">
          <span class="segment-metric-label">Satisfied %</span>
          <span class="segment-metric-value">${seg.satPct}%</span>
        </div>
        <div class="segment-metric">
          <span class="segment-metric-label">Avg Age</span>
          <span class="segment-metric-value">${seg.avgAge}</span>
        </div>
        <div class="segment-metric">
          <span class="segment-metric-label">Avg Prev Purchases</span>
          <span class="segment-metric-value">${seg.avgPrev}</span>
        </div>
      </div>
    `;
    container.appendChild(card);
  });
}

// ─────────────────────────────────────────────────────────────────────────────
// ICP (IDEAL CUSTOMER PROFILE)
// ─────────────────────────────────────────────────────────────────────────────

function renderICP() {
  const grid = $("#icp-grid");
  const icp = DATA.icp;

  const items = [
    { label: "Population Size", value: `${icp.count}`, detail: "19.4% of total customer base" },
    { label: "Avg Annual Spend", value: formatCurrency(icp.avgAnnualSpend), detail: "vs. $1,039 overall average" },
    { label: "Dominant Age Group", value: icp.topAgeGroup, detail: `Avg age: ${icp.avgAge} (range: ${icp.minAge}–${icp.maxAge})` },
    { label: "Gender Split", value: icp.dominantGender, detail: "vs. 68% Male overall" },
    { label: "Purchase Frequency", value: `${icp.avgFreq}×/yr`, detail: "Mostly weekly or fortnightly buyers" },
    { label: "Previous Purchases", value: `${icp.avgPrev} avg`, detail: "Deeply engaged with the brand" },
    { label: "Avg Review Rating", value: `${icp.avgRating} / 5.0`, detail: "70.8% rated ≥ 4.0 (satisfied)" },
    { label: "Subscription Rate", value: `${icp.subPct}%`, detail: "vs. 27% overall subscription rate" },
    { label: "Top Category", value: icp.topCategory, detail: "Followed by Accessories" },
    { label: "Payment Preference", value: icp.topPayment, detail: "Followed by PayPal, Cash" },
    { label: "Promo Usage", value: `${icp.promoPct}%`, detail: "Uses promos but NOT dependent on them" },
    { label: "Avg Order Value", value: `$${icp.avgPurchase}`, detail: "vs. $60 overall average" },
  ];

  items.forEach(item => {
    const el = createElement("div", "icp-item");
    el.innerHTML = `
      <div class="icp-item-label">${item.label}</div>
      <div class="icp-item-value">${item.value}</div>
      <div class="icp-item-detail">${item.detail}</div>
    `;
    grid.appendChild(el);
  });
}

// ─────────────────────────────────────────────────────────────────────────────
// INITIALIZE
// ─────────────────────────────────────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", () => {
  renderPyramid();
  renderScatter();
  renderGeo();
  renderFunnel();
  renderSegmentCards();
  renderICP();
});
