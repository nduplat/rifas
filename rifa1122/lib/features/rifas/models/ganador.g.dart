// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'ganador.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$GanadorImpl _$$GanadorImplFromJson(Map<String, dynamic> json) =>
    _$GanadorImpl(
      id: json['id'] as String,
      ticketId: json['ticketId'] as String,
      montoGanado: (json['montoGanado'] as num).toInt(),
      fechaPago: json['fechaPago'] == null
          ? null
          : DateTime.parse(json['fechaPago'] as String),
    );

Map<String, dynamic> _$$GanadorImplToJson(_$GanadorImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'ticketId': instance.ticketId,
      'montoGanado': instance.montoGanado,
      'fechaPago': instance.fechaPago?.toIso8601String(),
    };
