import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Upload from './components/upload';
import Download from './components/download';
import SignUp from './components/sign_up';

function App() {
  return (
    <Router>
      <div>
        <h1>Distributed File System</h1>
        <Routes>
          <Route path="/" element={<SignUp />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/download" element={<Download />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
