import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [similarInvoice, setSimilarInvoice] = useState(null);
  const [similarityScore, setSimilarityScore] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      setSimilarInvoice(response.data.most_similar_invoice);
      setSimilarityScore(response.data.similarity_score);
    } catch (error) {
      console.error("There was an error uploading the file!", error);
    }
  };

  return (
    <div className="App">
      <h1>Invoice Similarity Matching</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
      {similarInvoice && (
        <div>
          <h2>Most Similar Invoice</h2>
          <p>Invoice Number: {similarInvoice.invoice_number}</p>
          <p>Similarity Score: {similarityScore}</p>
          <h3>Invoice Text</h3>
          <p>{similarInvoice.text}</p>
        </div>
      )}
    </div>
  );
}

export default App;
