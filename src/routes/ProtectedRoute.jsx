import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const ProtectedRoute = ({ children }) => {
  const { auth } = useAuth();
  return auth.token ? children : <Navigate to="/" />;
};

export default ProtectedRoute;
