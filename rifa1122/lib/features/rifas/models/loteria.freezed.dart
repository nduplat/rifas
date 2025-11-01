// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'loteria.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

Loteria _$LoteriaFromJson(Map<String, dynamic> json) {
  return _Loteria.fromJson(json);
}

/// @nodoc
mixin _$Loteria {
  String get id => throw _privateConstructorUsedError;
  String get nombre => throw _privateConstructorUsedError;
  String? get descripcion => throw _privateConstructorUsedError;
  String get frecuencia => throw _privateConstructorUsedError;
  String? get urlResultados => throw _privateConstructorUsedError;

  /// Serializes this Loteria to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of Loteria
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $LoteriaCopyWith<Loteria> get copyWith => throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $LoteriaCopyWith<$Res> {
  factory $LoteriaCopyWith(Loteria value, $Res Function(Loteria) then) =
      _$LoteriaCopyWithImpl<$Res, Loteria>;
  @useResult
  $Res call({
    String id,
    String nombre,
    String? descripcion,
    String frecuencia,
    String? urlResultados,
  });
}

/// @nodoc
class _$LoteriaCopyWithImpl<$Res, $Val extends Loteria>
    implements $LoteriaCopyWith<$Res> {
  _$LoteriaCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of Loteria
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? nombre = null,
    Object? descripcion = freezed,
    Object? frecuencia = null,
    Object? urlResultados = freezed,
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
            descripcion: freezed == descripcion
                ? _value.descripcion
                : descripcion // ignore: cast_nullable_to_non_nullable
                      as String?,
            frecuencia: null == frecuencia
                ? _value.frecuencia
                : frecuencia // ignore: cast_nullable_to_non_nullable
                      as String,
            urlResultados: freezed == urlResultados
                ? _value.urlResultados
                : urlResultados // ignore: cast_nullable_to_non_nullable
                      as String?,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$LoteriaImplCopyWith<$Res> implements $LoteriaCopyWith<$Res> {
  factory _$$LoteriaImplCopyWith(
    _$LoteriaImpl value,
    $Res Function(_$LoteriaImpl) then,
  ) = __$$LoteriaImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    String id,
    String nombre,
    String? descripcion,
    String frecuencia,
    String? urlResultados,
  });
}

/// @nodoc
class __$$LoteriaImplCopyWithImpl<$Res>
    extends _$LoteriaCopyWithImpl<$Res, _$LoteriaImpl>
    implements _$$LoteriaImplCopyWith<$Res> {
  __$$LoteriaImplCopyWithImpl(
    _$LoteriaImpl _value,
    $Res Function(_$LoteriaImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of Loteria
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? nombre = null,
    Object? descripcion = freezed,
    Object? frecuencia = null,
    Object? urlResultados = freezed,
  }) {
    return _then(
      _$LoteriaImpl(
        id: null == id
            ? _value.id
            : id // ignore: cast_nullable_to_non_nullable
                  as String,
        nombre: null == nombre
            ? _value.nombre
            : nombre // ignore: cast_nullable_to_non_nullable
                  as String,
        descripcion: freezed == descripcion
            ? _value.descripcion
            : descripcion // ignore: cast_nullable_to_non_nullable
                  as String?,
        frecuencia: null == frecuencia
            ? _value.frecuencia
            : frecuencia // ignore: cast_nullable_to_non_nullable
                  as String,
        urlResultados: freezed == urlResultados
            ? _value.urlResultados
            : urlResultados // ignore: cast_nullable_to_non_nullable
                  as String?,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$LoteriaImpl implements _Loteria {
  const _$LoteriaImpl({
    required this.id,
    required this.nombre,
    this.descripcion,
    required this.frecuencia,
    this.urlResultados,
  });

  factory _$LoteriaImpl.fromJson(Map<String, dynamic> json) =>
      _$$LoteriaImplFromJson(json);

  @override
  final String id;
  @override
  final String nombre;
  @override
  final String? descripcion;
  @override
  final String frecuencia;
  @override
  final String? urlResultados;

  @override
  String toString() {
    return 'Loteria(id: $id, nombre: $nombre, descripcion: $descripcion, frecuencia: $frecuencia, urlResultados: $urlResultados)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$LoteriaImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.nombre, nombre) || other.nombre == nombre) &&
            (identical(other.descripcion, descripcion) ||
                other.descripcion == descripcion) &&
            (identical(other.frecuencia, frecuencia) ||
                other.frecuencia == frecuencia) &&
            (identical(other.urlResultados, urlResultados) ||
                other.urlResultados == urlResultados));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    id,
    nombre,
    descripcion,
    frecuencia,
    urlResultados,
  );

  /// Create a copy of Loteria
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$LoteriaImplCopyWith<_$LoteriaImpl> get copyWith =>
      __$$LoteriaImplCopyWithImpl<_$LoteriaImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$LoteriaImplToJson(this);
  }
}

abstract class _Loteria implements Loteria {
  const factory _Loteria({
    required final String id,
    required final String nombre,
    final String? descripcion,
    required final String frecuencia,
    final String? urlResultados,
  }) = _$LoteriaImpl;

  factory _Loteria.fromJson(Map<String, dynamic> json) = _$LoteriaImpl.fromJson;

  @override
  String get id;
  @override
  String get nombre;
  @override
  String? get descripcion;
  @override
  String get frecuencia;
  @override
  String? get urlResultados;

  /// Create a copy of Loteria
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$LoteriaImplCopyWith<_$LoteriaImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
