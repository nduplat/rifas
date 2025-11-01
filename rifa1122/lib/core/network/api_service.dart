import 'package:dio/dio.dart';
import 'package:rifa1122/network/auth_interceptor.dart';

class ApiService {
  late final Dio _dio;

  ApiService(String baseUrl) {
    _dio = Dio(BaseOptions(baseUrl: baseUrl));
    _dio.interceptors.add(AuthInterceptor());
  }

  Future<Response> get(String path, {Map<String, dynamic>? queryParameters}) async {
    return await _dio.get(path, queryParameters: queryParameters);
  }

  Future<Response> post(String path, {dynamic data, Map<String, dynamic>? queryParameters}) async {
    return await _dio.post(path, data: data, queryParameters: queryParameters);
  }

  Future<Response> put(String path, {dynamic data, Map<String, dynamic>? queryParameters}) async {
    return await _dio.put(path, data: data, queryParameters: queryParameters);
  }

  Future<Response> delete(String path, {Map<String, dynamic>? queryParameters}) async {
    return await _dio.delete(path, queryParameters: queryParameters);
  }
}