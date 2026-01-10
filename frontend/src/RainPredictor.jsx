import { useState } from "react";

export default function RainPredictor() {
  const [city, setCity] = useState("");
  const [state, setState] = useState("FL");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const predict = async () => {
    if (!city.trim()) {
      setError("Please enter a city name");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(
        `/predict?city=${encodeURIComponent(city)}&state=${state}`
      );

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || "Prediction failed");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h2>🌧️ Hourly Rain Predictor</h2>

      <div style={styles.form}>
        <input
          type="text"
          placeholder="Enter city (e.g. Miami)"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          style={styles.input}
        />

        <select
          value={state}
          onChange={(e) => setState(e.target.value)}
          style={styles.select}
        >
          <option value="FL">Florida</option>
        </select>

        <button onClick={predict} disabled={loading} style={styles.button}>
          {loading ? "Predicting..." : "Predict"}
        </button>
      </div>

      {error && <p style={styles.error}>⚠️ {error}</p>}

      {result && (
        <div style={styles.result}>
          <p>
            <strong>{result.city}, {result.state}</strong>
          </p>

          <p>
            Rain probability:{" "}
            <strong>{Math.round(result.rain_probability * 100)}%</strong>
          </p>

          <p style={{ fontSize: "1.2em" }}>
            {result.rain_next_hour ? "☔ Rain Likely" : "☀️ No Rain Expected"}
          </p>

          <p style={styles.meta}>
            Threshold: {result.threshold}
          </p>
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    maxWidth: 420,
    margin: "60px auto",
    padding: 20,
    fontFamily: "Arial, sans-serif",
    border: "1px solid #ddd",
    borderRadius: 8,
    textAlign: "center",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: 10,
  },
  input: {
    padding: 8,
    fontSize: 16,
  },
  select: {
    padding: 8,
    fontSize: 16,
  },
  button: {
    padding: 10,
    fontSize: 16,
    cursor: "pointer",
  },
  result: {
    marginTop: 20,
    padding: 15,
    background: "#f5f5f5",
    borderRadius: 6,
  },
  error: {
    color: "red",
    marginTop: 10,
  },
  meta: {
    fontSize: 12,
    color: "#666",
  },
};