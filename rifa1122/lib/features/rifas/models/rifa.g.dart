// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'rifa.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$RifaImpl _$$RifaImplFromJson(Map<String, dynamic> json) => _$RifaImpl(
  id: json['id'] as String,
  nombre: json['nombre'] as String,
  categoriaId: json['categoriaId'] as String,
  loteriaId: json['loteriaId'] as String,
  fechaInicio: DateTime.parse(json['fechaInicio'] as String),
  fechaFin: DateTime.parse(json['fechaFin'] as String),
  numeroGanadores: (json['numeroGanadores'] as num).toInt(),
  estado: json['estado'] as String,
);

Map<String, dynamic> _$$RifaImplToJson(_$RifaImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'nombre': instance.nombre,
      'categoriaId': instance.categoriaId,
      'loteriaId': instance.loteriaId,
      'fechaInicio': instance.fechaInicio.toIso8601String(),
      'fechaFin': instance.fechaFin.toIso8601String(),
      'numeroGanadores': instance.numeroGanadores,
      'estado': instance.estado,
    };
