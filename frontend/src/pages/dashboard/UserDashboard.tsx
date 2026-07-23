import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { reservaService, type Reserva } from '../../services/reserva.service';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Calendar, Search, Clock, CheckCircle, XCircle } from 'lucide-react';

export default function UserDashboard() {
  const { user } = useAuth();
  const [reservas, setReservas] = useState<Reserva[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    cargarReservas();
  }, []);

  const cargarReservas = async () => {
    try {
      setLoading(true);
      const data = await reservaService.listarMisReservas();
      setReservas(data);
    } catch (error) {
      console.error('Error al cargar reservas:', error);
    } finally {
      setLoading(false);
    }
  };

  const getEstadoIcon = (estado: string) => {
    switch (estado) {
      case 'PAGADA':
        return <CheckCircle className="w-5 h-5 text-green-600" />;
      case 'CANCELADA':
        return <XCircle className="w-5 h-5 text-red-600" />;
      case 'PENDIENTE':
        return <Clock className="w-5 h-5 text-yellow-600" />;
      default:
        return <Calendar className="w-5 h-5 text-blue-600" />;
    }
  };

  const getEstadoColor = (estado: string) => {
    switch (estado) {
      case 'PAGADA':
        return 'bg-green-100 text-green-800';
      case 'CANCELADA':
        return 'bg-red-100 text-red-800';
      case 'PENDIENTE':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-blue-100 text-blue-800';
    }
  };

  let reservasContenido;

  if (loading) {
    reservasContenido = (
      <div className="text-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
        <p className="mt-4 text-gray-600">Cargando reservas...</p>
      </div>
    );
  } else if (reservas.length === 0) {
    reservasContenido = (
      <div className="text-center py-8">
        <Calendar className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <p className="text-gray-600 mb-4">No tienes reservas aún</p>
        <Link to="/habitaciones">
          <Button>Buscar Habitaciones</Button>
        </Link>
      </div>
    );
  } else {
    reservasContenido = (
      <div className="space-y-4">
        {reservas.slice(0, 5).map((reserva) => (
          <div
            key={reserva.id}
            className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition"
          >
            <div className="flex items-center">
              {getEstadoIcon(reserva.estado)}
              <div className="ml-4">
                <p className="font-semibold">
                  Habitación #{reserva.habitacion_id}
                </p>
                <p className="text-sm text-gray-600">
                  {new Date(reserva.fecha_entrada).toLocaleDateString()} -{' '}
                  {new Date(reserva.fecha_salida).toLocaleDateString()}
                </p>
              </div>
            </div>
            <div className="text-right">
              <span
                className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${getEstadoColor(
                  reserva.estado
                )}`}
              >
                {reserva.estado}
              </span>
              <p className="text-lg font-bold text-primary mt-1">
                ${reserva.costo_total}
              </p>
            </div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-surface py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-display font-bold text-primary mb-2">
            Bienvenido, {user?.email}
          </h1>
          <p className="text-gray-600">
            Gestiona tus reservas y encuentra tu próxima estancia
          </p>
        </div>

        {/* Tarjetas de acceso rápido */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <Link to="/habitaciones">
            <Card className="hover:shadow-lg transition cursor-pointer">
              <CardContent className="pt-6">
                <div className="flex items-center">
                  <div className="bg-primary/10 p-4 rounded-lg mr-4">
                    <Search className="w-8 h-8 text-primary" />
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold mb-1">Buscar Habitaciones</h3>
                    <p className="text-gray-600 text-sm">
                      Encuentra la habitación perfecta para ti
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </Link>

          <Link to="/mis-reservas">
            <Card className="hover:shadow-lg transition cursor-pointer">
              <CardContent className="pt-6">
                <div className="flex items-center">
                  <div className="bg-primary/10 p-4 rounded-lg mr-4">
                    <Calendar className="w-8 h-8 text-primary" />
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold mb-1">Mis Reservas</h3>
                    <p className="text-gray-600 text-sm">
                      Gestiona y consulta tus reservas
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </Link>
        </div>

        {/* Reservas recientes */}
        <Card>
          <CardHeader>
            <CardTitle>Reservas Recientes</CardTitle>
          </CardHeader>
          <CardContent>
            {reservasContenido}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}