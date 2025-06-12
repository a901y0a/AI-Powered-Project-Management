import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { AuthProvider } from './context/AuthContext';
import './styles/chatbot.css';
import './styles/home.css';
import './styles/login.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
   
      <AuthProvider>
        <App />
      </AuthProvider>
    
  </React.StrictMode>
);
