import 'package:rifa1122/core/network/api_service.dart';
import 'package:rifa1122/features/rifas/models/rifa.dart';

class RifasRepository {
  final ApiService _apiService;

  RifasRepository(this._apiService);

  Future<List<Rifa>> getRifas() async {
    final response = await _apiService.get('/api/v1/rifas');
    final data = response.data as List<dynamic>;
    return data.map((json) => Rifa.fromJson(json)).toList();
  }
}