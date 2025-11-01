import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../../models/user.dart';

class AuthRepository {
  static const String _userKey = 'user';

  Future<User?> login(String name, String email) async {
    final prefs = await SharedPreferences.getInstance();
    final user = User(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      nombre: name,
      email: email,
      rol: 'jugador',
      creadoEn: DateTime.now(),
    );
    final userJson = jsonEncode(user.toJson());
    await prefs.setString(_userKey, userJson);
    return user;
  }

  Future<User?> register(String name, String email) async {
    final prefs = await SharedPreferences.getInstance();
    final user = User(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      nombre: name,
      email: email,
      rol: 'jugador',
      creadoEn: DateTime.now(),
    );
    final userJson = jsonEncode(user.toJson());
    await prefs.setString(_userKey, userJson);
    return user;
  }

  Future<User?> getCurrentUser() async {
    final prefs = await SharedPreferences.getInstance();
    final userJson = prefs.getString(_userKey);
    if (userJson != null) {
      final userMap = jsonDecode(userJson) as Map<String, dynamic>;
      return User.fromJson(userMap);
    }
    return null;
  }

  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_userKey);
  }
}