import React from 'react';

const ImageUploadForm = ({ handleSubmit, handleImageChange, image }) => {
  return (
    <form onSubmit={handleSubmit} className="form-style mt-4 npk-form">
      <div className="mb-3">
        <label htmlFor="fileImage" className="form-label">Enter your Image</label>
        <input
          type="file"
          className="form-control"
          name="fileImage"
          id="fileImage"
          accept="image/*"
          required
          onChange={handleImageChange}
        />
      </div>

      <div className="image-preview" id="imagePreview">
        {image ? <img src={URL.createObjectURL(image)} alt="Preview" className="img-fluid" /> : <p>No image selected</p>}
      </div>

      <button type="submit" className="btn btn-success w-100 mt-3">Predict</button>
    </form>
  );
};

export default ImageUploadForm;