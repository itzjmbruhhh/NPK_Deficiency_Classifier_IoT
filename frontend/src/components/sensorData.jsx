import { useState, useEffect } from "react";
import axios from "axios";

function SensorData() {
  const [sensorData, setSensorData] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/arduino/");
        console.log("Received sensor data:", response.data.sensor_data); // Add console log
        const data = response.data.sensor_data;
        setSensorData({
          Nitrogen: parseFloat(data.Nitrogen),
          Phosphorus: parseFloat(data.Phosphorus),
          Potassium: parseFloat(data.Potassium)
        });
      } catch (error) {
        console.error("Error fetching sensor data:", error);
      }
    };

    // Fetch data initially
    fetchData();

    // Set up interval to fetch data every 5 seconds
    const intervalId = setInterval(fetchData, 5000);

    // Clean up interval on component unmount
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-2xl font-bold mb-4">Live Sensor Data</h1>
      <div className="bg-white p-4 rounded shadow-md">
        <table className="table-auto">
          <thead>
            <tr>
              <th className="px-4 py-2">Nutrient</th>
              <th className="px-4 py-2">Value</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td className="border px-4 py-2">Nitrogen</td>
              <td className="border px-4 py-2">{sensorData.Nitrogen}</td>
            </tr>
            <tr>
              <td className="border px-4 py-2">Phosphorus</td>
              <td className="border px-4 py-2">{sensorData.Phosphorus}</td>
            </tr>
            <tr>
              <td className="border px-4 py-2">Potassium</td>
              <td className="border px-4 py-2">{sensorData.Potassium}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default SensorData;