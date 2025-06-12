import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import Chatbot from './components/Chatbot';
import Home from './components/Home';
import Login from './components/Login';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './routes/ProtectedRoute';
import './styles/chatbot.css';
import './styles/home.css';
import './styles/login.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/home" element={<ProtectedRoute><Home /></ProtectedRoute>} />
          <Route path="/chatbot" element={<ProtectedRoute><Chatbot /></ProtectedRoute>} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
