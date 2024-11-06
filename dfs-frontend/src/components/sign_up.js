import React, { useState } from 'react';
import axios from 'axios';

function SignUp() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSignUp = async () => {
    try {
      await axios.post('/api/signup', { username, password });
      alert('User profile created successfully!');
    } catch (error) {
      console.error(error);
      alert('Error creating user profile');
    }
  };

  return (
    <div>
      <h2>Create User Profile</h2>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleSignUp}>Sign Up</button>
    </div>
  );
}

export default SignUp;
