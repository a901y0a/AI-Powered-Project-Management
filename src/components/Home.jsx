import 'boxicons/css/boxicons.min.css';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/home.css';

const Home = () => {
  const navigate = useNavigate();
  const { auth, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <div className="homepage">
      <header className="navbar">
        <div className="navbar-container">
          <a href="#" className="brand-title">Hexaware</a>
          <ul className="nav-links">
            <li className="nav-item">Home</li>
            <li className="nav-item">About Us</li>
            <li className="nav-item">Projects</li>
            <li className="nav-item">Team</li>
            <li className="nav-item cta-btn" onClick={handleLogout}>Logout</li>
          </ul>
        </div>
      </header>

      <div className="home">
        <h2>Welcome to Project Management System</h2>
        <h3 style={{ marginTop: '20px' }}>Role: {auth.role}</h3>
      </div>

      <div style={{ padding: "20px" }} className="hero-section">
        <div className="hero-content">
          <div className="hero-text">
            <h1>Explore Project Details</h1>
            <p>
              The AI-Powered System digitizes and streamlines project tracking and team collaboration,
              enabling efficient planning, real-time monitoring, resource management, and performance analysis.
            </p>
            <button className="query-button" onClick={() => navigate('/chatbot')}>Ask a Query</button>
          </div>
          <div className="hero-image">
            <img src="https://api.pictographic.io/images/notion/P05UDsdcYnlZCzsC8O0T.svg" alt="Project Overview" className="main-illustration" />
          </div>
        </div>
      </div>

      <div className="chatbot-wrapper">
        <button className="chatbot-button" onClick={() => navigate('/chatbot')}>
          <i className="bx bx-message-rounded-dots"></i>
        </button>
      </div>
    </div>
  );
};

export default Home;
