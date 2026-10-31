let chartInstance = null;

async function predict() {
  const country = document.getElementById("country").value.trim() || "Selected Country";
  const rank = parseFloat(document.getElementById("rank").value);
  const y2000 = parseFloat(document.getElementById("y2000").value);
  const y2008 = parseFloat(document.getElementById("y2008").value);
  const y2015 = parseFloat(document.getElementById("y2015").value);
  const y2023 = parseFloat(document.getElementById("y2023").value);

  if (isNaN(rank) || isNaN(y2000) || isNaN(y2008) || isNaN(y2015) || isNaN(y2023)) {
    alert("Please fill in all years (2000, 2008, 2015, 2023) and global rank.");
    return;
  }

  const data = { rank, y2000, y2008, y2015, y2023 };

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    const result = await response.json();
    const risk = result.prediction;

    const resultElement = document.getElementById("result");
    resultElement.innerHTML = `
      <strong>${country}</strong>: Predicted Risk Level &rarr; 
      <span class="risk-highlight risk-${risk.toLowerCase()}">${risk}</span>
      <span class="trend-note">(${result.trend || 'Trend Calculated'})</span>
    `;

    renderTrendChart(country, [y2000, y2008, y2015, y2023], risk);
  } catch (err) {
    console.error("Prediction failed:", err);
  }
}

function renderTrendChart(country, yearsData, risk) {
  const canvas = document.getElementById("chart");
  if (!canvas) return;

  if (chartInstance) {
    chartInstance.destroy();
  }

  const riskColors = {
    low: "#10b981",
    moderate: "#f59e0b",
    serious: "#f97316",
    alarming: "#ef4444"
  };

  const color = riskColors[risk.toLowerCase()] || "#6366f1";

  chartInstance = new Chart(canvas, {
    type: "line",
    data: {
      labels: ["2000", "2008", "2015", "2023"],
      datasets: [
        {
          label: `${country} - Global Hunger Index (GHI)`,
          data: yearsData,
          borderColor: color,
          backgroundColor: color + "22",
          fill: true,
          tension: 0.35,
          pointRadius: 6,
          pointHoverRadius: 8
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          title: { display: true, text: "GHI Score (Lower is Better)" },
          beginAtZero: true
        }
      }
    }
  });
}
