import { useState } from "react";
import axios from "axios";

const Form = () => {
  const [formData, setFormData] = useState({
    Nitrogen: "",
    Phosphorus: "",
    Potassium: "",
    temperature: "",
    humidity: "",
    pH: "",
    rainfall: "",
  });

  const [prediction, setPrediction] = useState("");
  const [error, setError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setPrediction("");
    try {
      const response = await axios.post(
        `${import.meta.env.VITE_FLASK_API_URL}/api/predict`,
        formData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      setPrediction(response.data?.prediction || "No prediction received.");
    } catch (error) {
      console.error("Error:", error);
      setError(error.response?.data?.error || "Error fetching prediction.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-bl from-green-600 to-yellow-400 p-6">
      <div className="bg-white/20 backdrop-blur-lg shadow-xl rounded-2xl p-8 w-full max-w-2xl">
        <h1 className="text-3xl font-extrabold text-white text-center mb-8">🌱 Smart Crop Predictor</h1>
        <form onSubmit={handleSubmit} className="space-y-6">
          {Object.entries(formData).map(([key, value]) => (
            <div key={key}>
              <label htmlFor={key} className="block text-white text-lg font-medium capitalize">{key}</label>
              <input
                type="number"
                id={key}
                name={key}
                value={value}
                onChange={handleChange}
                required
                step="0.1"
                className="w-full p-3 rounded-lg bg-white/30 text-white focus:ring-4 focus:ring-green-500 placeholder-white"
                placeholder={`Enter ${key}`}
              />
            </div>
          ))}
          <button
            type="submit"
            className="w-full bg-green-600 hover:bg-green-700 text-white py-3 rounded-xl font-bold transition"
          >
            Get Prediction
          </button>
        </form>
        {prediction && (
          <p className="text-center mt-6 text-xl text-white font-semibold">
            Prediction: {prediction}
          </p>
        )}
        {error && (
          <p className="text-center mt-6 text-xl text-red-400 font-semibold">
            Error: {error}
          </p>
        )}
      </div>
    </div>
  );
};

export default Form;
