import axios from 'axios';

const API_URL = `http://127.0.0.1:8000/api/auth/api/auth`;

const login = async (username, password) => {
  try {
    const response = await axios.post(`${API_URL}/login`, {
      username,
      password,
    });

    if (response.data && response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user_role', response.data.role);
    }

    return response.data;
  } catch (error) {
    console.error('Login failed:', error.response?.data?.detail || error.message);
    throw error;
  }
};

const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user_role');
};

const getToken = () => {
  return localStorage.getItem('token');
};

const getUserRole = () => {
  return localStorage.getItem('user_role');
};

export default {
  login,
  logout,
  getToken,
  getUserRole,
};
