import React, { useState } from "react";
import axios from "axios";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import "./App.css";
import ImageUploadForm from "./components/ImageUploadForm";
import PredictionResult from "./components/PredictionResult";
import SensorData from "./components/sensorData"; // Import SensorData component

function App() {
  const [image, setImage] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [confidence, setConfidence] = useState(null);

  const handleImageChange = (event) => {
    setImage(event.target.files[0]);
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append("fileImage", image);

    axios
      .post("http://127.0.0.1:8000/api/predict/", formData, {
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
        },
      })
      .then((response) => {
        const data = response.data;
        if (data.success) {
          setPrediction(data.prediction);
          setConfidence(data.confidence);
        } else {
          alert("Prediction failed. Please try again.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("An error occurred. Please try again.");
      });
  };

  const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  };

  return (
    <Router>
      <div className="App">
        <nav className="navbar navbar-expand-lg navbar-light bg-light fixed-top">
          <div className="container">
            <h1>Leaf NPK Classification</h1>
          </div>
        </nav>

        <div className="container mt-5 pt-5">
          <PredictionResult
            prediction={prediction}
            confidence={confidence}
          />
          <Routes>
            <Route
              path="/"
              element={
                <div className="content-wrapper">
                  <div className="npk-classifier">
                    <h2>Upload an Image for Prediction</h2>
                    <ImageUploadForm
                      handleSubmit={handleSubmit}
                      handleImageChange={handleImageChange}
                      image={image}
                    />
                  </div>
                  <div className="sensor-data">
                    <SensorData /> {/* Display SensorData component on the main page */}
                  </div>
                </div>
              }
            />
            <Route path="/sensor" element={<SensorData />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;