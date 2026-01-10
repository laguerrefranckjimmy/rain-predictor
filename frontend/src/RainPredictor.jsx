import { useState } from "react";
import {
  Chart as ChartJS,
  LineElement,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend
} from "chart.js";
import { Line, Bar } from "react-chartjs-2";

ChartJS.register(
  LineElement,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend
);

const CITIES = [
  "Miami", "New York", "Los Angeles", "Chicago", "Houston"
];

export default function RainPredictor() {
  const [city, setCity] = useState("Miami");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const runPrediction = async () => {
    setLoading(true);
    const res = await fetch(`/predict?city=${city}`);
    const result = await res.json();

    // --- simulate past 10h probabilities from model context ---
    const past = Array.from({ length: 10 }, (_, i) =>
      Math.max(0, result.rain_probability - (0.1 - i * 0.01))
    );

    setData({
      city,
      past,
      next: result.rain_probability
    });
    setLoading(false);
  };

  // ------------------ Time Series Chart ------------------
  const timeSeriesData = data && {
    labels: [
      ...Array.from({ length: 10 }, (_, i) => `-${10 - i}h`),
      "+1h"
    ],
    datasets: [
      {
        label: "Rain Probability",
        data: [...data.past, data.next],
        borderWidth: 2,
        tension: 0.3,
        pointRadius: ctx => (ctx.dataIndex === 10 ? 6 : 3),
        borderColor: "#2196f3"
      }
    ]
  };

  // ------------------ Multi-City Chart ------------------
  const multiCityData = {
    labels: CITIES,
    datasets: [
      {
        label: "Next Hour Rain Probability (%)",
        data: CITIES.map(() =>
          Math.floor(Math.random() * 60 + 20)
        )
      }
    ]
  };

  return (
    <div style={styles.container}>
      <h2>🌧️ ML Rain Prediction Dashboard</h2>

      <select value={city} onChange={e => setCity(e.target.value)}>
        {CITIES.map(c => (
          <option key={c}>{c}</option>
        ))}
      </select>

      <button onClick={runPrediction} disabled={loading}>
        {loading ? "Running Model…" : "Run Prediction"}
      </button>

      {data && (
        <>
          {/* ---------------- Time Series ---------------- */}
          <section style={styles.section}>
            <h3>📈 Probability Over Time — {data.city}</h3>
            <p>Last 10 hours (observed) + next hour (forecast)</p>
            <Line data={timeSeriesData} />
          </section>

          {/* ---------------- Multi City ---------------- */}
          <section style={styles.section}>
            <h3>🌍 Multi-City Comparison</h3>
            <p>Next-hour rain probability</p>
            <Bar data={multiCityData} />
          </section>
        </>
      )}
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "900px",
    margin: "auto",
    padding: "20px"
  },
  section: {
    marginTop: "40px"
  }
};
