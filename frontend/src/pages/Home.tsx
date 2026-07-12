import { Search, Calendar, MapPin } from 'lucide-react';

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="relative h-[70vh] overflow-hidden">
        {/* Imagen de fondo */}
        <div 
          className="absolute inset-0 bg-cover bg-center"
          style={{
            backgroundImage: 'url(https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80)',
          }}
        >
          <div className="absolute inset-0 bg-black/30"></div>
        </div>

        {/* Barra de búsqueda */}
        <div className="relative h-full flex items-center justify-center px-4">
          <div className="bg-white rounded-xl shadow-lg p-6 w-full max-w-4xl">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Lugar */}
              <div className="relative">
                <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  placeholder="¿A dónde vas?"
                  className="w-full pl-10 pr-4 py-3 border-2 border-gray-200 rounded-lg focus:border-primary focus:outline-none transition"
                />
              </div>

              {/* Fecha */}
              <div className="relative">
                <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="date"
                  className="w-full pl-10 pr-4 py-3 border-2 border-gray-200 rounded-lg focus:border-primary focus:outline-none transition"
                />
              </div>

              {/* Botón buscar */}
              <button className="flex items-center justify-center space-x-2 bg-primary text-white py-3 px-6 rounded-lg hover:bg-secondary transition shadow-md hover:shadow-lg">
                <Search className="w-5 h-5" />
                <span className="font-semibold">Buscar</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Título */}
      <div className="max-w-7xl mx-auto px-4 py-16 text-center">
        <h1 className="text-5xl font-display font-bold text-primary mb-4">
          Reserva tu habitación ya
        </h1>
        <p className="text-xl text-gray-600">
          Encuentra las mejores ofertas en hoteles de todo el mundo
        </p>
      </div>
    </div>
  );
}