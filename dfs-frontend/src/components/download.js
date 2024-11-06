// components/Download.js
import React, { useState } from 'react';
import axios from 'axios';

function Download() {
  const [fileName, setFileName] = useState('');

  const handleDownload = async () => {
    try {
      const response = await axios.get(`/api/download/${fileName}`, {
        responseType: 'blob', // Important for downloading files
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', fileName);
      document.body.appendChild(link);
      link.click();
    } catch (error) {
      console.error(error);
      alert('Error downloading file');
    }
  };

  return (
    <div>
      <h2>Download a File</h2>
      <input
        type="text"
        placeholder="Enter filename"
        value={fileName}
        onChange={(e) => setFileName(e.target.value)}
      />
      <button onClick={handleDownload}>Download</button>
    </div>
  );
}

export default Download;
