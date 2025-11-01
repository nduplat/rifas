import 'package:freezed_annotation/freezed_annotation.dart';

part 'ganador.freezed.dart';
part 'ganador.g.dart';

@freezed
class Ganador with _$Ganador {
  const factory Ganador({
    required String id,
    required String ticketId,
    required int montoGanado,
    DateTime? fechaPago,
  }) = _Ganador;

  factory Ganador.fromJson(Map<String, dynamic> json) => _$GanadorFromJson(json);
}

/// Example JSON:
/// {
///   "id": "550e8400-e29b-41d4-a716-446655440005",
///   "ticket_id": "550e8400-e29b-41d4-a716-446655440004",
///   "monto_ganado": 187500,
///   "fecha_pago": "2023-12-25T10:00:00.000Z"
/// }