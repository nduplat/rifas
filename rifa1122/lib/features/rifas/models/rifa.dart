import 'package:freezed_annotation/freezed_annotation.dart';

part 'rifa.freezed.dart';
part 'rifa.g.dart';

@freezed
class Rifa with _$Rifa {
  const factory Rifa({
    required String id,
    required String nombre,
    required String categoriaId,
    required String loteriaId,
    required DateTime fechaInicio,
    required DateTime fechaFin,
    required int numeroGanadores,
    required String estado,
  }) = _Rifa;

  factory Rifa.fromJson(Map<String, dynamic> json) => _$RifaFromJson(json);
}

/// Example JSON:
/// {
///   "id": "550e8400-e29b-41d4-a716-446655440003",
///   "nombre": "Rifa Especial Navidad",
///   "categoria_id": "550e8400-e29b-41d4-a716-446655440002",
///   "loteria_id": "550e8400-e29b-41d4-a716-446655440001",
///   "fecha_inicio": "2023-12-01T00:00:00.000Z",
///   "fecha_fin": "2023-12-24T23:59:59.000Z",
///   "numero_ganadores": 2,
///   "estado": "activa"
/// }