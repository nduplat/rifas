// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'categoria_rifa.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$CategoriaRifaImpl _$$CategoriaRifaImplFromJson(Map<String, dynamic> json) =>
    _$CategoriaRifaImpl(
      id: json['id'] as String,
      nombre: json['nombre'] as String,
      color: json['color'] as String,
      valorBoleta: (json['valorBoleta'] as num).toInt(),
      totalRecaudo: (json['totalRecaudo'] as num).toInt(),
      rake: (json['rake'] as num).toDouble(),
      fondoPremios: (json['fondoPremios'] as num).toInt(),
      premioPorGanador: (json['premioPorGanador'] as num).toInt(),
      comentario: json['comentario'] as String?,
    );

Map<String, dynamic> _$$CategoriaRifaImplToJson(_$CategoriaRifaImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'nombre': instance.nombre,
      'color': instance.color,
      'valorBoleta': instance.valorBoleta,
      'totalRecaudo': instance.totalRecaudo,
      'rake': instance.rake,
      'fondoPremios': instance.fondoPremios,
      'premioPorGanador': instance.premioPorGanador,
      'comentario': instance.comentario,
    };
