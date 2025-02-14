import React from 'react';

const PredictionResult = ({ prediction, confidence }) => {
  return (
    prediction && (
      <div className="alert alert-info mt-4">
        <strong>Prediction:</strong> The image is classified as <strong>{prediction}</strong>.
        <br />
        <strong>Confidence Level:</strong> {confidence}%
      </div>
    )
  );
};

export default PredictionResult;