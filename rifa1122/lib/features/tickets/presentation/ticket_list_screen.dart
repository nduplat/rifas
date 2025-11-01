import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:rifa1122/core/network/mock_api_service.dart';
import 'package:rifa1122/features/tickets/data/ticket_repository.dart';
import 'package:rifa1122/features/rifas/models/ticket.dart';

// Provider for TicketRepository
final ticketRepositoryProvider = Provider<TicketRepository>((ref) {
  final apiService = ref.watch(mockApiServiceProvider);
  return TicketRepository(apiService);
});

// Provider for fetching user's tickets
final userTicketsProvider = FutureProvider.family<List<Ticket>, String>((ref, userId) async {
  final repository = ref.watch(ticketRepositoryProvider);
  return repository.obtenerTickets(userId);
});

class TicketListScreen extends ConsumerWidget {
  final String userId;

  const TicketListScreen({super.key, required this.userId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final ticketsAsync = ref.watch(userTicketsProvider(userId));

    return Scaffold(
      appBar: AppBar(
        title: const Text('Mis Boletos'),
      ),
      body: ticketsAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, stack) => Center(child: Text('Error: $error')),
        data: (tickets) {
          if (tickets.isEmpty) {
            return const Center(child: Text('No tienes boletos comprados'));
          }
          return ListView.builder(
            itemCount: tickets.length,
            itemBuilder: (context, index) {
              final ticket = tickets[index];
              return ListTile(
                title: Text('Número: ${ticket.numero.toString().padLeft(3, '0')}'),
                subtitle: Text('Estado: ${ticket.estado}'),
                trailing: Text('Comprado: ${ticket.compradoEn.toLocal().toString().split(' ')[0]}'),
              );
            },
          );
        },
      ),
    );
  }
}