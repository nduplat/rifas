// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'rifa.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

Rifa _$RifaFromJson(Map<String, dynamic> json) {
  return _Rifa.fromJson(json);
}

/// @nodoc
mixin _$Rifa {
  String get id => throw _privateConstructorUsedError;
  String get nombre => throw _privateConstructorUsedError;
  String get categoriaId => throw _privateConstructorUsedError;
  String get loteriaId => throw _privateConstructorUsedError;
  DateTime get fechaInicio => throw _privateConstructorUsedError;
  DateTime get fechaFin => throw _privateConstructorUsedError;
  int get numeroGanadores => throw _privateConstructorUsedError;
  String get estado => throw _privateConstructorUsedError;

  /// Serializes this Rifa to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of Rifa
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $RifaCopyWith<Rifa> get copyWith => throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $RifaCopyWith<$Res> {
  factory $RifaCopyWith(Rifa value, $Res Function(Rifa) then) =
      _$RifaCopyWithImpl<$Res, Rifa>;
  @useResult
  $Res call({
    String id,
    String nombre,
    String categoriaId,
    String loteriaId,
    DateTime fechaInicio,
    DateTime fechaFin,
    int numeroGanadores,
    String estado,
  });
}

/// @nodoc
class _$RifaCopyWithImpl<$Res, $Val extends Rifa>
    implements $RifaCopyWith<$Res> {
  _$RifaCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of Rifa
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? nombre = null,
    Object? categoriaId = null,
    Object? loteriaId = null,
    Object? fechaInicio = null,
    Object? fechaFin = null,
    Object? numeroGanadores = null,
    Object? estado = null,
  }) {
    return _then(
      _value.copyWith(
            id: null == id
                ? _value.id
                : id // ignore: cast_nullable_to_non_nullable
                      as String,
            nombre: null == nombre
                ? _value.nombre
                : nombre // ignore: cast_nullable_to_non_nullable
                      as String,
            categoriaId: null == categoriaId
                ? _value.categoriaId
                : categoriaId // ignore: cast_nullable_to_non_nullable
                      as String,
            loteriaId: null == loteriaId
                ? _value.loteriaId
                : loteriaId // ignore: cast_nullable_to_non_nullable
                      as String,
            fechaInicio: null == fechaInicio
                ? _value.fechaInicio
                : fechaInicio // ignore: cast_nullable_to_non_nullable
                      as DateTime,
            fechaFin: null == fechaFin
                ? _value.fechaFin
                : fechaFin // ignore: cast_nullable_to_non_nullable
                      as DateTime,
            numeroGanadores: null == numeroGanadores
                ? _value.numeroGanadores
                : numeroGanadores // ignore: cast_nullable_to_non_nullable
                      as int,
            estado: null == estado
                ? _value.estado
                : estado // ignore: cast_nullable_to_non_nullable
                      as String,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$RifaImplCopyWith<$Res> implements $RifaCopyWith<$Res> {
  factory _$$RifaImplCopyWith(
    _$RifaImpl value,
    $Res Function(_$RifaImpl) then,
  ) = __$$RifaImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    String id,
    String nombre,
    String categoriaId,
    String loteriaId,
    DateTime fechaInicio,
    DateTime fechaFin,
    int numeroGanadores,
    String estado,
  });
}

/// @nodoc
class __$$RifaImplCopyWithImpl<$Res>
    extends _$RifaCopyWithImpl<$Res, _$RifaImpl>
    implements _$$RifaImplCopyWith<$Res> {
  __$$RifaImplCopyWithImpl(_$RifaImpl _value, $Res Function(_$RifaImpl) _then)
    : super(_value, _then);

  /// Create a copy of Rifa
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? nombre = null,
    Object? categoriaId = null,
    Object? loteriaId = null,
    Object? fechaInicio = null,
    Object? fechaFin = null,
    Object? numeroGanadores = null,
    Object? estado = null,
  }) {
    return _then(
      _$RifaImpl(
        id: null == id
            ? _value.id
            : id // ignore: cast_nullable_to_non_nullable
                  as String,
        nombre: null == nombre
            ? _value.nombre
            : nombre // ignore: cast_nullable_to_non_nullable
                  as String,
        categoriaId: null == categoriaId
            ? _value.categoriaId
            : categoriaId // ignore: cast_nullable_to_non_nullable
                  as String,
        loteriaId: null == loteriaId
            ? _value.loteriaId
            : loteriaId // ignore: cast_nullable_to_non_nullable
                  as String,
        fechaInicio: null == fechaInicio
            ? _value.fechaInicio
            : fechaInicio // ignore: cast_nullable_to_non_nullable
                  as DateTime,
        fechaFin: null == fechaFin
            ? _value.fechaFin
            : fechaFin // ignore: cast_nullable_to_non_nullable
                  as DateTime,
        numeroGanadores: null == numeroGanadores
            ? _value.numeroGanadores
            : numeroGanadores // ignore: cast_nullable_to_non_nullable
                  as int,
        estado: null == estado
            ? _value.estado
            : estado // ignore: cast_nullable_to_non_nullable
                  as String,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$RifaImpl implements _Rifa {
  const _$RifaImpl({
    required this.id,
    required this.nombre,
    required this.categoriaId,
    required this.loteriaId,
    required this.fechaInicio,
    required this.fechaFin,
    required this.numeroGanadores,
    required this.estado,
  });

  factory _$RifaImpl.fromJson(Map<String, dynamic> json) =>
      _$$RifaImplFromJson(json);

  @override
  final String id;
  @override
  final String nombre;
  @override
  final String categoriaId;
  @override
  final String loteriaId;
  @override
  final DateTime fechaInicio;
  @override
  final DateTime fechaFin;
  @override
  final int numeroGanadores;
  @override
  final String estado;

  @override
  String toString() {
    return 'Rifa(id: $id, nombre: $nombre, categoriaId: $categoriaId, loteriaId: $loteriaId, fechaInicio: $fechaInicio, fechaFin: $fechaFin, numeroGanadores: $numeroGanadores, estado: $estado)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$RifaImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.nombre, nombre) || other.nombre == nombre) &&
            (identical(other.categoriaId, categoriaId) ||
                other.categoriaId == categoriaId) &&
            (identical(other.loteriaId, loteriaId) ||
                other.loteriaId == loteriaId) &&
            (identical(other.fechaInicio, fechaInicio) ||
                other.fechaInicio == fechaInicio) &&
            (identical(other.fechaFin, fechaFin) ||
                other.fechaFin == fechaFin) &&
            (identical(other.numeroGanadores, numeroGanadores) ||
                other.numeroGanadores == numeroGanadores) &&
            (identical(other.estado, estado) || other.estado == estado));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    id,
    nombre,
    categoriaId,
    loteriaId,
    fechaInicio,
    fechaFin,
    numeroGanadores,
    estado,
  );

  /// Create a copy of Rifa
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$RifaImplCopyWith<_$RifaImpl> get copyWith =>
      __$$RifaImplCopyWithImpl<_$RifaImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$RifaImplToJson(this);
  }
}

abstract class _Rifa implements Rifa {
  const factory _Rifa({
    required final String id,
    required final String nombre,
    required final String categoriaId,
    required final String loteriaId,
    required final DateTime fechaInicio,
    required final DateTime fechaFin,
    required final int numeroGanadores,
    required final String estado,
  }) = _$RifaImpl;

  factory _Rifa.fromJson(Map<String, dynamic> json) = _$RifaImpl.fromJson;

  @override
  String get id;
  @override
  String get nombre;
  @override
  String get categoriaId;
  @override
  String get loteriaId;
  @override
  DateTime get fechaInicio;
  @override
  DateTime get fechaFin;
  @override
  int get numeroGanadores;
  @override
  String get estado;

  /// Create a copy of Rifa
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$RifaImplCopyWith<_$RifaImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
