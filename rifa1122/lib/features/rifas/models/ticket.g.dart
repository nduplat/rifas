// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'ticket.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$TicketImpl _$$TicketImplFromJson(Map<String, dynamic> json) => _$TicketImpl(
  id: json['id'] as String,
  rifaId: json['rifaId'] as String,
  usuarioId: json['usuarioId'] as String,
  numero: (json['numero'] as num).toInt(),
  compradoEn: DateTime.parse(json['compradoEn'] as String),
  estado: json['estado'] as String,
);

Map<String, dynamic> _$$TicketImplToJson(_$TicketImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'rifaId': instance.rifaId,
      'usuarioId': instance.usuarioId,
      'numero': instance.numero,
      'compradoEn': instance.compradoEn.toIso8601String(),
      'estado': instance.estado,
    };
