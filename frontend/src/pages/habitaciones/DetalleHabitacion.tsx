import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { habitacionService, type Habitacion } from '../../services/habitacion.service';
import { Card, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Users, DollarSign, Bed, ArrowLeft, Calendar } from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';

export default function DetalleHabitacion() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const [habitacion, setHabitacion] = useState<Habitacion | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      cargarHabitacion();
    }
  }, [id]);

  const cargarHabitacion = async () => {
    try {
      setLoading(true);
      const data = await habitacionService.obtenerPorId(parseInt(id!));
      setHabitacion(data);
    } catch (error) {
      console.error('Error al cargar habitación:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleReservar = () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    navigate(`/reservas/nueva?habitacion_id=${id}`);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-gray-600">Cargando habitación...</p>
        </div>
      </div>
    );
  }

  if (!habitacion) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">Habitación no encontrada</p>
          <Button onClick={() => navigate('/habitaciones')} className="mt-4">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Volver a habitaciones
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-surface py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <Button
          variant="ghost"
          onClick={() => navigate('/habitaciones')}
          className="mb-6"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Volver a habitaciones
        </Button>

        <Card>
          <CardContent className="pt-6">
            <div className="mb-6">
              <h1 className="text-3xl font-display font-bold text-primary mb-2">
                Habitación {habitacion.numero}
              </h1>
              <p className="text-xl text-gray-600 capitalize">{habitacion.tipo}</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
              <div>
                <div className="bg-gray-200 rounded-xl h-64 flex items-center justify-center mb-4">
                  <Bed className="w-24 h-24 text-gray-400" />
                </div>
              </div>

              <div>
                <h2 className="text-2xl font-semibold mb-4">Características</h2>
                <div className="space-y-3">
                  <div className="flex items-center text-gray-700">
                    <Users className="w-5 h-5 mr-3 text-primary" />
                    <span>Capacidad: {habitacion.capacidad || 2} personas</span>
                  </div>
                  <div className="flex items-center text-gray-700">
                    <Bed className="w-5 h-5 mr-3 text-primary" />
                    <span>Tipo: {habitacion.tipo}</span>
                  </div>
                  <div className="flex items-center text-gray-700">
                    <DollarSign className="w-5 h-5 mr-3 text-primary" />
                    <span className="text-2xl font-bold text-primary">
                      ${habitacion.precio}
                    </span>
                    <span className="text-gray-600 ml-2">/noche</span>
                  </div>
                </div>
              </div>
            </div>

            {habitacion.descripcion && (
              <div className="mb-8">
                <h2 className="text-2xl font-semibold mb-4">Descripción</h2>
                <p className="text-gray-700 leading-relaxed">{habitacion.descripcion}</p>
              </div>
            )}

            <div className="border-t border-gray-200 pt-6">
              <Button
                onClick={handleReservar}
                size="lg"
                className="w-full md:w-auto"
              >
                <Calendar className="w-5 h-5 mr-2" />
                Reservar esta habitación
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}