import api from './api';

export interface Habitacion {
  id: number;
  numero: string;
  tipo: string;
  precio: number;
  disponible: boolean;
  descripcion?: string;
  capacidad?: number;
}

export interface HabitacionSearchParams {
  tipo?: string;
  precio_min?: number;
  precio_max?: number;
  disponible?: boolean;
}

export interface HabitacionResponse {
  data: Habitacion[];
  total?: number;
  page?: number;
}

export const habitacionService = {
  listar: async (params?: HabitacionSearchParams): Promise<Habitacion[]> => {
    const response = await api.get<HabitacionResponse | Habitacion[]>('/api/habitaciones', { params });
    
    // Manejar ambos formatos: array directo o objeto con propiedad 'data'
    const responseData = response.data;
    
    if (Array.isArray(responseData)) {
      return responseData;
    } else if (responseData && Array.isArray(responseData.data)) {
      return responseData.data;
    } else {
      console.warn('Formato de respuesta inesperado:', responseData);
      return [];
    }
  },

  obtenerPorId: async (id: number) => {
    const response = await api.get<Habitacion>(`/api/habitaciones/${id}`);
    return response.data;
  },

  crear: async (data: Omit<Habitacion, 'id'>) => {
    const response = await api.post<Habitacion>('/api/habitaciones', data);
    return response.data;
  },

  cambiarEstado: async (id: number, disponible: boolean) => {
    const response = await api.patch<Habitacion>(`/api/habitaciones/${id}/estado`, { disponible });
    return response.data;
  },

  eliminar: async (id: number) => {
    await api.delete(`/api/habitaciones/${id}`);
  },
};