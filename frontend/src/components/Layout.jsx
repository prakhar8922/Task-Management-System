import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Layout.css';

const Layout = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isActive = (path) => location.pathname === path;

  return (
    <div className="layout">
      <nav className="navbar">
        <div className="nav-container">
          <Link to="/dashboard" className="nav-brand">
            📋 Task Manager
          </Link>
          
          <div className="nav-links">
            <Link 
              to="/dashboard" 
              className={isActive('/dashboard') ? 'nav-link active' : 'nav-link'}
            >
              Dashboard
            </Link>
            <Link 
              to="/projects" 
              className={isActive('/projects') || location.pathname.startsWith('/projects/') ? 'nav-link active' : 'nav-link'}
            >
              Projects
            </Link>
            <Link 
              to="/tasks" 
              className={isActive('/tasks') || location.pathname.startsWith('/tasks/') ? 'nav-link active' : 'nav-link'}
            >
              Tasks
            </Link>
          </div>

          <div className="nav-user">
            <span className="user-email">{user?.email}</span>
            <button onClick={handleLogout} className="btn btn-secondary">
              Logout
            </button>
          </div>
        </div>
      </nav>

      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;
