import { Shield, Clock, Users, Award } from 'lucide-react';

export default function About() {
  return (
    <div className="min-h-screen bg-background">
      {/* Header de la sección */}
      <div className="bg-primary text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-display font-bold mb-4">
            Sobre Nosotros
          </h1>
          <p className="text-lg text-gray-300 max-w-2xl mx-auto">
            Transformando la experiencia de reserva hotelera con tecnología moderna, 
            seguridad y eficiencia.
          </p>
        </div>
      </div>

      {/* Contenido principal */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center mb-16">
          <div>
            <h2 className="text-3xl font-display font-bold text-primary mb-6">
              Nuestra Misión
            </h2>
            <p className="text-gray-600 text-lg leading-relaxed mb-4">
              Desarrollar un sistema de reservas de hoteles robusto, intuitivo y seguro, 
              que permita a los usuarios encontrar y reservar sus habitaciones ideales 
              en cuestión de minutos, mientras proporciona a los administradores 
              herramientas poderosas para gestionar su inventario.
            </p>
            <p className="text-gray-600 text-lg leading-relaxed">
              Nuestro equipo está comprometido con la excelencia en el desarrollo de 
              soluciones tecnológicas que mejoren la experiencia de viaje de nuestros 
              usuarios en todo el mundo.
            </p>
          </div>
          <div className="bg-surface rounded-2xl p-8 shadow-md">
            <img 
              src="https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" 
              alt="Equipo de desarrollo" 
              className="rounded-xl w-full h-64 object-cover shadow-sm"
            />
          </div>
        </div>

        {/* Características del sistema */}
        <div className="text-center mb-12">
          <h2 className="text-3xl font-display font-bold text-primary mb-4">
            Características del Sistema
          </h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Construido con tecnologías de vanguardia para garantizar rendimiento y escalabilidad.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition">
            <Shield className="w-10 h-10 text-primary mb-4" />
            <h3 className="text-xl font-semibold mb-2">Seguridad</h3>
            <p className="text-gray-600 text-sm">Autenticación JWT y encriptación de datos sensibles.</p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition">
            <Clock className="w-10 h-10 text-primary mb-4" />
            <h3 className="text-xl font-semibold mb-2">Tiempo Real</h3>
            <p className="text-gray-600 text-sm">Disponibilidad de habitaciones actualizada al instante.</p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition">
            <Users className="w-10 h-10 text-primary mb-4" />
            <h3 className="text-xl font-semibold mb-2">Multi-rol</h3>
            <p className="text-gray-600 text-sm">Interfaces diferenciadas para usuarios y administradores.</p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition">
            <Award className="w-10 h-10 text-primary mb-4" />
            <h3 className="text-xl font-semibold mb-2">Calidad</h3>
            <p className="text-gray-600 text-sm">Pruebas automatizadas y arquitectura robusta.</p>
          </div>
        </div>
      </div>
    </div>
  );
}