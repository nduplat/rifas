// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'user.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$UserImpl _$$UserImplFromJson(Map<String, dynamic> json) => _$UserImpl(
  id: json['id'] as String,
  nombre: json['nombre'] as String,
  email: json['email'] as String,
  telefono: json['telefono'] as String?,
  rol: json['rol'] as String,
  creadoEn: DateTime.parse(json['creadoEn'] as String),
);

Map<String, dynamic> _$$UserImplToJson(_$UserImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'nombre': instance.nombre,
      'email': instance.email,
      'telefono': instance.telefono,
      'rol': instance.rol,
      'creadoEn': instance.creadoEn.toIso8601String(),
    };
