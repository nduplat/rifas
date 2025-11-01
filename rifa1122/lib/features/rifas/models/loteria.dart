import 'package:freezed_annotation/freezed_annotation.dart';

part 'loteria.freezed.dart';
part 'loteria.g.dart';

@freezed
class Loteria with _$Loteria {
  const factory Loteria({
    required String id,
    required String nombre,
    String? descripcion,
    required String frecuencia,
    String? urlResultados,
  }) = _Loteria;

  factory Loteria.fromJson(Map<String, dynamic> json) => _$LoteriaFromJson(json);
}

/// Example JSON:
/// {
///   "id": "550e8400-e29b-41d4-a716-446655440001",
///   "nombre": "Baloto",
///   "descripcion": "Lotería nacional colombiana",
///   "frecuencia": "semanal",
///   "url_resultados": "https://www.baloto.com/resultados"
/// }