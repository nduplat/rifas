import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class AuthInterceptor extends Interceptor {
  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) async {
    final token = await _storage.read(key: 'access_token');
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    super.onRequest(options, handler);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) async {
    if (err.response?.statusCode == 401) {
      // Token expired, try to refresh
      final refreshToken = await _storage.read(key: 'refresh_token');
      if (refreshToken != null) {
        try {
          final dio = Dio();
          final response = await dio.post('/auth/refresh', data: {
            'refresh_token': refreshToken,
          });

          if (response.statusCode == 200) {
            final newToken = response.data['access_token'];
            await _storage.write(key: 'access_token', value: newToken);

            // Retry the original request with new token
            final newOptions = err.requestOptions;
            newOptions.headers['Authorization'] = 'Bearer $newToken';
            final newResponse = await dio.fetch(newOptions);
            return handler.resolve(newResponse);
          }
        } catch (e) {
          // Refresh failed, logout
          await _storage.delete(key: 'access_token');
          await _storage.delete(key: 'refresh_token');
        }
      }
    }
    super.onError(err, handler);
  }
}