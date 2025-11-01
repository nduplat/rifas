import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class AuthService {
  final Dio _dio;
  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  AuthService(this._dio);

  Future<String?> login(String email, String password) async {
    try {
      final response = await _dio.post('/auth/login', data: {
        'email': email,
        'password': password,
      });

      if (response.statusCode == 200) {
        final token = response.data['access_token'];
        await _saveToken(token);
        return token;
      }
    } catch (e) {
      throw Exception('Login failed: $e');
    }
    return null;
  }

  Future<void> logout() async {
    await _deleteToken();
  }

  Future<void> _saveToken(String token) async {
    await _storage.write(key: 'access_token', value: token);
  }

  Future<String?> getToken() async {
    return await _storage.read(key: 'access_token');
  }

  Future<void> _deleteToken() async {
    await _storage.delete(key: 'access_token');
  }

  Future<bool> isLoggedIn() async {
    final token = await getToken();
    return token != null;
  }
}