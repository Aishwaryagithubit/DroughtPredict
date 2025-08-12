// This is a simple single-file React-like app using vanilla JS for simplicity.
// If you prefer React + Vite, convert this component accordingly.

/*const root = document.getElementById('root');

root.innerHTML = `
  <div class="container">
    <h1>Drought & Water Prediction Demo</h1>
    <div id="form"></div>
    <div id="result"></div>
  </div>
`;

const form = document.getElementById('form');
form.innerHTML = `
  <div class="row">
    <input id="city" class="input" placeholder="City (e.g. Kathmandu)" />
    <input id="population" class="input" placeholder="Population" type="number" />
  </div>
  <div class="row">
    <input id="rainfall_mm" class="input" placeholder="Rainfall (mm)" type="number" />
    <input id="avg_temp_c" class="input" placeholder="Avg Temp (°C)" type="number" />
  </div>
  <div class="row">
    <input id="soil_moisture" class="input" placeholder="Soil moisture" type="number" />
    <input id="reservoir_level" class="input" placeholder="Reservoir level" type="number" />
  </div>
  <div class="row">
    <input id="past_month_consumption" class="input" placeholder="Past month consumption (m3)" type="number"/>
    <button id="predictBtn" class="btn">Get Prediction</button>
  </div>
  <div class="row">
    <input id="email" class="input" placeholder="Email to subscribe for alerts (optional)"/>
    <button id="subscribeBtn" class="btn">Subscribe</button>
  </div>
`;

const result = document.getElementById('result');

document.getElementById('predictBtn').addEventListener('click', async () => {
  const payload = {
    city: document.getElementById('city').value || "Unknown",
    rainfall_mm: Number(document.getElementById('rainfall_mm').value || 0),
    avg_temp_c: Number(document.getElementById('avg_temp_c').value || 0),
    soil_moisture: Number(document.getElementById('soil_moisture').value || 0),
    reservoir_level: Number(document.getElementById('reservoir_level').value || 0),
    population: Number(document.getElementById('population').value || 100000),
    past_month_consumption: Number(document.getElementById('past_month_consumption').value || 0),
  };
  result.innerHTML = `<div class="small">Contacting server...</div>`;
  try {
    const r = await fetch("/predict", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify(payload)
    });
    const json = await r.json();
    result.innerHTML = `
      <div class="result">
        <div><strong>City:</strong> ${json.city}</div>
        <div><strong>Drought probability:</strong> ${(json.drought_probability*100).toFixed(1)}%</div>
        <div><strong>Predicted demand (m³):</strong> ${json.predicted_demand_m3.toFixed(0)}</div>
        <div><strong>Predicted supply (m³):</strong> ${json.predicted_supply_m3.toFixed(0)}</div>
        <div class="small">Use <em>Check Alerts</em> to evaluate and notify subscribers if thresholds are exceeded.</div>
        <button id="checkBtn" class="btn" style="margin-top:0.6rem;">Check Alerts (notify)</button>
      </div>
    `;
    document.getElementById('checkBtn').addEventListener('click', async () => {
      result.innerHTML = `<div class="small">Running alert check...</div>`;
      const rr = await fetch("/check-alerts", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify(payload)
      });
      const resjson = await rr.json();
      result.innerHTML = `<div class="result"><pre>${JSON.stringify(resjson, null, 2)}</pre></div>`;
    });
  } catch (e) {
    result.innerHTML = `<div class="result">Error: ${e.message}</div>`;
  }
});

document.getElementById('subscribeBtn').addEventListener('click', async () => {
  const city = document.getElementById('city').value || "Unknown";
  const email = document.getElementById('email').value || null;
  result.innerHTML = `<div class="small">Subscribing ${email} for ${city}...</div>`;
  try {
    const r = await fetch("/subscribe", {
      method:"POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({city, email})
    });
    const j = await r.json();
    result.innerHTML = `<div class="result"><pre>${JSON.stringify(j, null, 2)}</pre></div>`;
  } catch (e) {
    result.innerHTML = `<div class="result">Subscribe error: ${e.message}</div>`;
  }
});
*/