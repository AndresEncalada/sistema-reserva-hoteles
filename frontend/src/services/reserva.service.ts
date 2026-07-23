import api from './api';

export interface Reserva {
  id: number;
  usuario_id: string;
  habitacion_id: number;
  fecha_entrada: string;
  fecha_salida: string;
  estado: 'PENDIENTE' | 'CONFIRMADA' | 'PAGADA' | 'CANCELADA';
  costo_total: number;
  fecha_creacion: string;
}

export interface CrearReservaRequest {
  habitacion_id: number;
  fecha_entrada: string;
  fecha_salida: string;
}

export const reservaService = {
  crear: async (data: CrearReservaRequest) => {
    const response = await api.post<Reserva>('/reservas', data);
    return response.data;
  },

  listarMisReservas: async () => {
    const response = await api.get<Reserva[]>('/reservas/mis-reservas');
    return response.data;
  },

  cancelar: async (id: number) => {
    const response = await api.patch<Reserva>(`/reservas/${id}/cancelar`);
    return response.data;
  },

  notificarPago: async (id: number) => {
    const response = await api.post<Reserva>(`/reservas/${id}/notificar-pago`);
    return response.data;
  },

  // Métodos de administrador
  listarTodas: async () => {
    const response = await api.get<Reserva[]>('/reservas');
    return response.data;
  },

  marcarPagado: async (id: number) => {
    const response = await api.patch<Reserva>(`/reservas/${id}/pagar`);
    return response.data;
  },
};