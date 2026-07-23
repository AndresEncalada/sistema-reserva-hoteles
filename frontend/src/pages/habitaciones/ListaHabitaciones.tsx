import { useState, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { habitacionService, type Habitacion } from '../../services/habitacion.service';
import { Card, CardContent } from '../../components/ui/Card';
import { Input } from '../../components/ui/Input';
import { Button } from '../../components/ui/Button';
import { Search, Users, DollarSign, Bed, AlertCircle } from 'lucide-react';

export default function ListaHabitaciones() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [habitaciones, setHabitaciones] = useState<Habitacion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const [filtroTipo, setFiltroTipo] = useState(searchParams.get('destino') || '');
  const [filtroPrecioMax, setFiltroPrecioMax] = useState(searchParams.get('precio_max') || '');

  useEffect(() => {
    cargarHabitaciones();
  }, []);

  const cargarHabitaciones = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const params: any = { disponible: true };
      if (filtroTipo) params.tipo = filtroTipo;
      if (filtroPrecioMax) params.precio_max = parseFloat(filtroPrecioMax);
      
      const data = await habitacionService.listar(params);
      setHabitaciones(data);
    } catch (err: any) {
      console.error('Error al cargar habitaciones:', err);
      setError(err.response?.data?.detail || 'Error al cargar las habitaciones. Intenta nuevamente.');
      setHabitaciones([]);
    } finally {
      setLoading(false);
    }
  };

  const handleBuscar = (e: React.FormEvent) => {
    e.preventDefault();
    const newParams = new URLSearchParams();
    if (filtroTipo) newParams.set('destino', filtroTipo);
    if (filtroPrecioMax) newParams.set('precio_max', filtroPrecioMax);
    setSearchParams(newParams);
    
    cargarHabitaciones();
  };

  // Extraemos la lógica condicional en una variable para evitar ternarios anidados
  let content;

  if (loading) {
    content = (
      <div className="text-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
        <p className="mt-4 text-gray-600">Cargando habitaciones...</p>
      </div>
    );
  } else if (habitaciones.length === 0) {
    content = (
      <div className="text-center py-12 bg-white rounded-xl border border-gray-200">
        <Bed className="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h3 className="text-xl font-semibold text-gray-700 mb-2">
          No se encontraron habitaciones
        </h3>
        <p className="text-gray-500 mb-6">
          Intenta ajustar los filtros de búsqueda o verifica más tarde.
        </p>
        <Button onClick={() => { 
          setFiltroTipo(''); 
          setFiltroPrecioMax(''); 
          setSearchParams(''); 
          cargarHabitaciones(); 
        }}>
          Limpiar filtros
        </Button>
      </div>
    );
  } else {
    content = (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {habitaciones.map((habitacion) => (
          <Link key={habitacion.id} to={`/habitaciones/${habitacion.id}`}>
            <Card className="h-full hover:shadow-lg transition cursor-pointer group">
              <CardContent className="pt-6">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-xl font-semibold text-primary group-hover:text-primary/80 transition">
                      Habitación {habitacion.numero}
                    </h3>
                    <p className="text-gray-600 capitalize">{habitacion.tipo}</p>
                  </div>
                  <Bed className="w-8 h-8 text-gray-300 group-hover:text-primary transition" />
                </div>

                {habitacion.descripcion && (
                  <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                    {habitacion.descripcion}
                  </p>
                )}

                <div className="flex items-center justify-between pt-4 border-t border-gray-100">
                  <div className="flex items-center text-gray-600">
                    <Users className="w-4 h-4 mr-1" />
                    <span className="text-sm">{habitacion.capacidad || 2} personas</span>
                  </div>
                  <div className="flex items-center text-primary font-bold">
                    <DollarSign className="w-4 h-4" />
                    <span className="text-xl">{habitacion.precio}</span>
                    <span className="text-sm text-gray-600 ml-1">/noche</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-surface py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-display font-bold text-primary mb-4">
            Habitaciones Disponibles
          </h1>
          <p className="text-gray-600">
            Encuentra la habitación perfecta para tu estancia
          </p>
        </div>

        {/* Filtros */}
        <Card className="mb-8">
          <CardContent className="pt-6">
            <form onSubmit={handleBuscar} className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Tipo de habitación
                </label>
                <select
                  value={filtroTipo}
                  onChange={(e) => setFiltroTipo(e.target.value)}
                  className="w-full px-3 py-2 border-2 border-gray-200 rounded-lg focus:border-primary focus:outline-none bg-white"
                >
                  <option value="">Todos los tipos</option>
                  <option value="individual">Individual</option>
                  <option value="doble">Doble</option>
                  <option value="suite">Suite</option>
                  <option value="familiar">Familiar</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Precio máximo por noche
                </label>
                <Input
                  type="number"
                  value={filtroPrecioMax}
                  onChange={(e) => setFiltroPrecioMax(e.target.value)}
                  placeholder="Ej: 200"
                />
              </div>

              <div className="flex items-end">
                <Button type="submit" className="w-full" disabled={loading}>
                  <Search className="w-4 h-4 mr-2" />
                  {loading ? 'Buscando...' : 'Buscar'}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>

        {/* Estado de Error */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-4 rounded-lg flex items-center gap-3 mb-6">
            <AlertCircle className="w-5 h-5 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Renderizado del contenido condicional */}
        {content}
      </div>
    </div>
  );
}