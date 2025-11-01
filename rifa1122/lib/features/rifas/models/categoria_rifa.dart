import 'package:freezed_annotation/freezed_annotation.dart';

part 'categoria_rifa.freezed.dart';
part 'categoria_rifa.g.dart';

@freezed
class CategoriaRifa with _$CategoriaRifa {
  const factory CategoriaRifa({
    required String id,
    required String nombre,
    required String color,
    required int valorBoleta,
    required int totalRecaudo,
    required double rake,
    required int fondoPremios,
    required int premioPorGanador,
    String? comentario,
  }) = _CategoriaRifa;

  factory CategoriaRifa.fromJson(Map<String, dynamic> json) => _$CategoriaRifaFromJson(json);
}

/// Example JSON:
/// {
///   "id": "550e8400-e29b-41d4-a716-446655440002",
///   "nombre": "Bronce",
///   "color": "Marrón",
///   "valor_boleta": 5000,
///   "total_recaudo": 500000,
///   "rake": 0.25,
///   "fondo_premios": 375000,
///   "premio_por_ganador": 187500,
///   "comentario": "Premium"
/// }