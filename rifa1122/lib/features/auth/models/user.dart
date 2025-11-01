import 'package:freezed_annotation/freezed_annotation.dart';

part 'user.freezed.dart';
part 'user.g.dart';

@freezed
class User with _$User {
  const factory User({
    required String id,
    required String nombre,
    required String email,
    String? telefono,
    required String rol,
    required DateTime creadoEn,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}

/// Example JSON:
/// {
///   "id": "550e8400-e29b-41d4-a716-446655440000",
///   "nombre": "Juan Pérez",
///   "email": "juan@example.com",
///   "telefono": "+57 300 123 4567",
///   "rol": "jugador",
///   "creado_en": "2023-10-01T10:00:00.000Z"
/// }