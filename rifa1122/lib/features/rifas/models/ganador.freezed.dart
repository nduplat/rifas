// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'ganador.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

Ganador _$GanadorFromJson(Map<String, dynamic> json) {
  return _Ganador.fromJson(json);
}

/// @nodoc
mixin _$Ganador {
  String get id => throw _privateConstructorUsedError;
  String get ticketId => throw _privateConstructorUsedError;
  int get montoGanado => throw _privateConstructorUsedError;
  DateTime? get fechaPago => throw _privateConstructorUsedError;

  /// Serializes this Ganador to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of Ganador
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $GanadorCopyWith<Ganador> get copyWith => throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $GanadorCopyWith<$Res> {
  factory $GanadorCopyWith(Ganador value, $Res Function(Ganador) then) =
      _$GanadorCopyWithImpl<$Res, Ganador>;
  @useResult
  $Res call({String id, String ticketId, int montoGanado, DateTime? fechaPago});
}

/// @nodoc
class _$GanadorCopyWithImpl<$Res, $Val extends Ganador>
    implements $GanadorCopyWith<$Res> {
  _$GanadorCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of Ganador
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? ticketId = null,
    Object? montoGanado = null,
    Object? fechaPago = freezed,
  }) {
    return _then(
      _value.copyWith(
            id: null == id
                ? _value.id
                : id // ignore: cast_nullable_to_non_nullable
                      as String,
            ticketId: null == ticketId
                ? _value.ticketId
                : ticketId // ignore: cast_nullable_to_non_nullable
                      as String,
            montoGanado: null == montoGanado
                ? _value.montoGanado
                : montoGanado // ignore: cast_nullable_to_non_nullable
                      as int,
            fechaPago: freezed == fechaPago
                ? _value.fechaPago
                : fechaPago // ignore: cast_nullable_to_non_nullable
                      as DateTime?,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$GanadorImplCopyWith<$Res> implements $GanadorCopyWith<$Res> {
  factory _$$GanadorImplCopyWith(
    _$GanadorImpl value,
    $Res Function(_$GanadorImpl) then,
  ) = __$$GanadorImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({String id, String ticketId, int montoGanado, DateTime? fechaPago});
}

/// @nodoc
class __$$GanadorImplCopyWithImpl<$Res>
    extends _$GanadorCopyWithImpl<$Res, _$GanadorImpl>
    implements _$$GanadorImplCopyWith<$Res> {
  __$$GanadorImplCopyWithImpl(
    _$GanadorImpl _value,
    $Res Function(_$GanadorImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of Ganador
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? ticketId = null,
    Object? montoGanado = null,
    Object? fechaPago = freezed,
  }) {
    return _then(
      _$GanadorImpl(
        id: null == id
            ? _value.id
            : id // ignore: cast_nullable_to_non_nullable
                  as String,
        ticketId: null == ticketId
            ? _value.ticketId
            : ticketId // ignore: cast_nullable_to_non_nullable
                  as String,
        montoGanado: null == montoGanado
            ? _value.montoGanado
            : montoGanado // ignore: cast_nullable_to_non_nullable
                  as int,
        fechaPago: freezed == fechaPago
            ? _value.fechaPago
            : fechaPago // ignore: cast_nullable_to_non_nullable
                  as DateTime?,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$GanadorImpl implements _Ganador {
  const _$GanadorImpl({
    required this.id,
    required this.ticketId,
    required this.montoGanado,
    this.fechaPago,
  });

  factory _$GanadorImpl.fromJson(Map<String, dynamic> json) =>
      _$$GanadorImplFromJson(json);

  @override
  final String id;
  @override
  final String ticketId;
  @override
  final int montoGanado;
  @override
  final DateTime? fechaPago;

  @override
  String toString() {
    return 'Ganador(id: $id, ticketId: $ticketId, montoGanado: $montoGanado, fechaPago: $fechaPago)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$GanadorImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.ticketId, ticketId) ||
                other.ticketId == ticketId) &&
            (identical(other.montoGanado, montoGanado) ||
                other.montoGanado == montoGanado) &&
            (identical(other.fechaPago, fechaPago) ||
                other.fechaPago == fechaPago));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode =>
      Object.hash(runtimeType, id, ticketId, montoGanado, fechaPago);

  /// Create a copy of Ganador
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$GanadorImplCopyWith<_$GanadorImpl> get copyWith =>
      __$$GanadorImplCopyWithImpl<_$GanadorImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$GanadorImplToJson(this);
  }
}

abstract class _Ganador implements Ganador {
  const factory _Ganador({
    required final String id,
    required final String ticketId,
    required final int montoGanado,
    final DateTime? fechaPago,
  }) = _$GanadorImpl;

  factory _Ganador.fromJson(Map<String, dynamic> json) = _$GanadorImpl.fromJson;

  @override
  String get id;
  @override
  String get ticketId;
  @override
  int get montoGanado;
  @override
  DateTime? get fechaPago;

  /// Create a copy of Ganador
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$GanadorImplCopyWith<_$GanadorImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
