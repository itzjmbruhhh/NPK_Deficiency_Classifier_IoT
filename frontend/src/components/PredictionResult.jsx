import React from 'react';

const PredictionResult = ({ prediction, confidence }) => {
  if (!prediction) return null;

  const renderResult = () => {
    if (confidence >= 90) {
      return (
        <div className="alert alert-info mt-4">
          <strong>Prediction:</strong> The image is classified as <strong>{prediction}</strong>.
          <br />
          <strong>Confidence Level:</strong> {confidence}%
        </div>
      );
    } else {
      return (
        <div className="alert alert-danger mt-4">
          <strong>Cannot classify. Please retake the image.</strong>
        </div>
      );
    }
  };

  return renderResult();
};

export default PredictionResult;