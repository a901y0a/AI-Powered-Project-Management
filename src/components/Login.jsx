import axios from 'axios';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const res = await axios.post("http://127.0.0.1:8000/api/auth/login", {
  username,
  password
});

      login(res.data.access_token, res.data.role);
      navigate('/home');
    } catch {
      setError('Invalid credentials');
    }
  };

  return (
    <div className="login-page">
      <h2>ProjectAI Login</h2>
      <form className="login-form" onSubmit={handleSubmit}>
        <input type="text" placeholder="Username" value={username}
          onChange={e => setUsername(e.target.value)} required />
        <input type="password" placeholder="Password" value={password}
          onChange={e => setPassword(e.target.value)} required />
        <button type="submit">Login</button>
        {error && <p className="error-msg">{error}</p>}
      </form>
    </div>
  );
};

export default Login;
