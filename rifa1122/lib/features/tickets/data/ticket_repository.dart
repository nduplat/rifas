import 'package:rifa1122/core/network/api_service.dart';
import 'package:rifa1122/features/rifas/models/ticket.dart';

class TicketRepository {
  final ApiService _apiService;

  TicketRepository(this._apiService);

  Future<Ticket> comprarBoleta(String rifaId, String userId) async {
    final ticketData = {
      'rifaId': rifaId,
      'usuarioId': userId,
    };
    final response = await _apiService.post('/api/v1/tickets', data: ticketData);
    return Ticket.fromJson(response.data);
  }

  Future<List<Ticket>> obtenerTickets(String userId) async {
    final response = await _apiService.get('/api/v1/tickets', queryParameters: {'usuarioId': userId});
    final data = response.data as List<dynamic>;
    return data.map((json) => Ticket.fromJson(json)).toList();
  }
}