import { Link } from 'react-router-dom';
import { User, LogIn } from 'lucide-react';

export default function Navbar() {
  const isAuthenticated = false;

  return (
    <nav className="bg-white shadow-sm border-b border-gray-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo con hover atractivo */}
          <Link to="/" className="logo-link relative inline-block">
            <span className="text-2xl font-display font-bold text-primary">
              Hoteles.com
            </span>
          </Link>

          {/* Menú derecho */}
          <div className="flex items-center space-x-8">
            {/* Sobre Nosotros con hover de línea */}
            <Link 
              to="/sobre-nosotros" 
              className="nav-link relative text-sm font-medium text-gray-700 hover:text-primary transition-colors"
            >
              Sobre Nosotros
            </Link>

            {/* Botón Login/Usuario con hover de INVERSIÓN */}
            {isAuthenticated ? (
              <button className="btn-primary flex items-center space-x-2 px-5 py-2.5 bg-primary text-white rounded-lg border-2 border-primary transition-all shadow-sm">
                <User className="w-4 h-4" />
                <span className="text-sm font-medium">Mi Cuenta</span>
              </button>
            ) : (
              <Link 
                to="/login" 
                className="btn-primary flex items-center space-x-2 px-5 py-2.5 bg-primary text-white rounded-lg border-2 border-primary transition-all shadow-sm"
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