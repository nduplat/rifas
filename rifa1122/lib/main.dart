import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_stripe/flutter_stripe.dart';
import 'package:go_router/go_router.dart';
import 'package:rifa1122/core/network/api_service.dart';
import 'package:rifa1122/core/theme/app_theme.dart';
import 'package:rifa1122/features/auth/data/auth_repository.dart';
import 'package:rifa1122/features/rifas/data/rifas_repository.dart';
import 'package:rifa1122/features/rifas/presentation/rifa_list_screen.dart';
import 'package:rifa1122/features/rifas/presentation/rifa_detail_screen.dart';
import 'package:rifa1122/features/tickets/data/ticket_repository.dart';
import 'package:rifa1122/features/tickets/presentation/ticket_list_screen.dart';
import 'package:rifa1122/features/auth/presentation/login_screen.dart';
import 'package:rifa1122/services/auth_service.dart';
import 'package:dio/dio.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  Stripe.publishableKey = 'pk_test_...'; // Replace with your Stripe publishable key
  runApp(const ProviderScope(child: MyApp()));
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'Rifa1122',
      theme: appTheme,
      routerConfig: _router,
    );
  }
}

// Providers
final authServiceProvider = Provider<AuthService>((ref) {
  final dio = Dio(BaseOptions(baseUrl: 'http://localhost:8000'));
  return AuthService(dio);
});

final apiServiceProvider = Provider<ApiService>((ref) {
  const baseUrl = String.fromEnvironment('BASE_URL', defaultValue: 'http://localhost:8000');
  return ApiService(baseUrl);
});

final rifasRepositoryProvider = Provider<RifasRepository>((ref) {
  final apiService = ref.watch(apiServiceProvider);
  return RifasRepository(apiService);
});

final ticketRepositoryProvider = Provider<TicketRepository>((ref) {
  final apiService = ref.watch(apiServiceProvider);
  return TicketRepository(apiService);
});

final GoRouter _router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const RifaListScreen(),
    ),
    GoRoute(
      path: '/rifa/:id',
      builder: (context, state) => RifaDetailScreen(rifaId: state.pathParameters['id']!),
    ),
    GoRoute(
      path: '/tickets',
      builder: (context, state) => const TicketListScreen(userId: 'user-123'), // Assuming hardcoded userId for demo
    ),
    GoRoute(
      path: '/login',
      builder: (context, state) => const LoginScreen(),
    ),
  ],
);
