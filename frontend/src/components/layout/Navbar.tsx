import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { User, LogIn, LogOut, ChevronDown } from 'lucide-react';
import { useState } from 'react';

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="bg-white shadow-sm border-b border-gray-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="logo-link relative inline-block">
            <span className="text-2xl font-display font-bold text-primary">
              Hoteles.com
            </span>
          </Link>

          {/* Menú derecho */}
          <div className="flex items-center space-x-8">
            {/* Sobre Nosotros */}
            <Link
              to="/sobre-nosotros"
              className="nav-link relative text-sm font-medium text-gray-700 hover:text-primary transition-colors"
            >
              Sobre Nosotros
            </Link>

            {/* Botón Login/Usuario */}
            {isAuthenticated ? (
              <div className="relative">
                <button
                  onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                  className="flex items-center space-x-2 px-4 py-2 bg-primary text-white rounded-lg hover:bg-white hover:text-primary border-2 border-primary transition-all shadow-sm hover:shadow-md hover:-translate-y-0.5"
                >
                  <User className="w-4 h-4" />
                  <span className="text-sm font-medium">{user?.email}</span>
                  <ChevronDown className="w-4 h-4" />
                </button>

                {/* Dropdown */}
                {isDropdownOpen && (
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-100 py-1">
                    <Link
                      to="/dashboard"
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition"
                      onClick={() => setIsDropdownOpen(false)}
                    >
                      Mi Dashboard
                    </Link>
                    {user?.role === 'ADMIN' && (
                      <Link
                        to="/admin"
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition"
                        onClick={() => setIsDropdownOpen(false)}
                      >
                        Panel Admin
                      </Link>
                    )}
                    <Link
                      to="/perfil"
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition"
                      onClick={() => setIsDropdownOpen(false)}
                    >
                      Mi Perfil
                    </Link>
                    <button
                      onClick={handleLogout}
                      className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition flex items-center gap-2"
                    >
                      <LogOut className="w-4 h-4" />
                      Cerrar Sesión
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <Link
                to="/login"
                className="flex items-center space-x-2 px-5 py-2.5 bg-primary text-white rounded-lg border-2 border-primary hover:bg-white hover:text-primary transition-all shadow-sm hover:shadow-md hover:-translate-y-0.5"
              >
                <LogIn className="w-4 h-4" />
                <span className="text-sm font-medium">Iniciar Sesión</span>
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}