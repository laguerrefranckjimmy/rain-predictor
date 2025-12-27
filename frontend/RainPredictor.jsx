import { useState } from "react";

export default function RainPredictor() {
  const [city, setCity] = useState("");
  const [result, setResult] = useState(null);

  const predict = async () => {
    const res = await fetch(`http://localhost:8000/predict?city=${city}`);
    setResult(await res.json());
  };

  return (
    <div>
      <h2>🌧️ Rain Predictor</h2>
      <input onChange={e => setCity(e.target.value)} />
      <button onClick={predict}>Predict</button>

      {result && (
        <p>
          {result.rain_probability * 100}% —
          {result.rain_next_hour ? "☔ Rain Likely" : "☀️ No Rain"}
        </p>
      )}
    </div>
  );
}
