import { Hotel, Mail, Phone, MapPin } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Footer() {
    return (
        <footer className="bg-primary text-white mt-auto">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
                    {/* Marca */}
                    <div className="col-span-1 md:col-span-1">
                        <div className="flex items-center space-x-2 mb-4">
                            <Hotel className="w-6 h-6" />
                            <span className="text-xl font-display font-bold">Hoteles.com</span>
                        </div>
                        <p className="text-gray-400 text-sm leading-relaxed">
                            La plataforma más confiable para reservar tu próxima estancia con las mejores tarifas garantizadas.
                        </p>
                    </div>

                    {/* Enlaces rápidos */}
                    <div>
                        <h4 className="text-sm font-semibold uppercase tracking-wider mb-4">Enlaces</h4>
                        <ul className="space-y-2">
                            <li><Link to="/" className="text-gray-400 hover:text-white transition text-sm">Inicio</Link></li>
                            <li><Link to="/sobre-nosotros" className="text-gray-400 hover:text-white transition text-sm">Sobre Nosotros</Link></li>
                            <li><Link to="/login" className="text-gray-400 hover:text-white transition text-sm">Iniciar Sesión</Link></li>
                        </ul>
                    </div>

                    {/* Soporte */}
                    <div>
                        <h4 className="text-sm font-semibold uppercase tracking-wider mb-4">Soporte</h4>
                        <ul className="space-y-2">
                            <li><a href="#" className="text-gray-400 hover:text-white transition text-sm">Centro de Ayuda</a></li>
                            <li><a href="#" className="text-gray-400 hover:text-white transition text-sm">Términos y Condiciones</a></li>
                            <li><a href="#" className="text-gray-400 hover:text-white transition text-sm">Política de Privacidad</a></li>
                        </ul>
                    </div>

                    {/* Contacto */}
                    <div>
                        <h4 className="text-sm font-semibold uppercase tracking-wider mb-4">Contacto</h4>
                        <ul className="space-y-3">
                            <li className="flex items-center space-x-2 text-gray-400 text-sm">
                                <MapPin className="w-4 h-4" />
                                <span>Cuenca, Ecuador</span>
                            </li>
                            <li className="flex items-center space-x-2 text-gray-400 text-sm">
                                <Mail className="w-4 h-4" />
                                <span>contacto@hoteles.com</span>
                            </li>
                            <li className="flex items-center space-x-2 text-gray-400 text-sm">
                                <Phone className="w-4 h-4" />
                                <span>+593 2 123 4567</span>
                            </li>
                        </ul>
                    </div>
                </div>

                {/* Línea divisoria y copyright */}
                <div className="border-t border-gray-800 mt-12 pt-8 text-center">
                    <p className="text-gray-500 text-sm">
                        © {new Date().getFullYear()} Hoteles.com. Todos los derechos reservados.
                    </p>
                </div>
            </div>
        </footer>
    );
}