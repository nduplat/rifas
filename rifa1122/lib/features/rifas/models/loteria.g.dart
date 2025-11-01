// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'loteria.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$LoteriaImpl _$$LoteriaImplFromJson(Map<String, dynamic> json) =>
    _$LoteriaImpl(
      id: json['id'] as String,
      nombre: json['nombre'] as String,
      descripcion: json['descripcion'] as String?,
      frecuencia: json['frecuencia'] as String,
      urlResultados: json['urlResultados'] as String?,
    );

Map<String, dynamic> _$$LoteriaImplToJson(_$LoteriaImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'nombre': instance.nombre,
      'descripcion': instance.descripcion,
      'frecuencia': instance.frecuencia,
      'urlResultados': instance.urlResultados,
    };
