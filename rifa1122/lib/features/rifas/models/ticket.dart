import 'package:freezed_annotation/freezed_annotation.dart';

part 'ticket.freezed.dart';
part 'ticket.g.dart';

@freezed
class Ticket with _$Ticket {
  const factory Ticket({
    required String id,
    required String rifaId,
    required String usuarioId,
    required int numero,
    required DateTime compradoEn,
    required String estado,
  }) = _Ticket;

  factory Ticket.fromJson(Map<String, dynamic> json) => _$TicketFromJson(json);
}

/// Example JSON:
/// {
///   "id": "550e8400-e29b-41d4-a716-446655440004",
///   "rifa_id": "550e8400-e29b-41d4-a716-446655440003",
///   "usuario_id": "550e8400-e29b-41d4-a716-446655440000",
///   "numero": 42,
///   "comprado_en": "2023-12-01T14:30:00.000Z",
///   "estado": "vendido"
/// }