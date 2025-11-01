import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_stripe/flutter_stripe.dart';
import 'package:rifa1122/features/rifas/models/rifa.dart';
import 'package:rifa1122/features/rifas/models/categoria_rifa.dart';

// Provider for fetching single rifa by id
final rifaByIdProvider = FutureProvider.family<Rifa?, String>((ref, rifaId) async {
  final apiService = ref.watch(apiServiceProvider);
  final response = await apiService.get('/api/v1/rifas/$rifaId');
  final data = response.data as Map<String, dynamic>;
  return Rifa.fromJson(data);
});

// Provider for fetching categorias
final categoriasProvider = FutureProvider<List<CategoriaRifa>>((ref) async {
  final apiService = ref.watch(apiServiceProvider);
  final response = await apiService.get('/api/v1/categorias');
  final data = response.data as List<dynamic>;
  return data.map((json) => CategoriaRifa.fromJson(json)).toList();
});

// Provider to get categoria by id
final categoriaByIdProvider = Provider.family<CategoriaRifa?, String>((ref, categoriaId) {
  final categoriasAsync = ref.watch(categoriasProvider);
  return categoriasAsync.maybeWhen(
    data: (categorias) => categorias.firstWhere(
      (categoria) => categoria.id == categoriaId,
      orElse: () => null,
    ),
    orElse: () => null,
  );
});

class RifaDetailScreen extends ConsumerWidget {
  final String rifaId;

  const RifaDetailScreen({super.key, required this.rifaId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final rifaAsync = ref.watch(rifaByIdProvider(rifaId));

    return Scaffold(
      appBar: AppBar(
        title: const Text('Detalles de Rifa'),
      ),
      body: rifaAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, stack) => Center(child: Text('Error: $error')),
        data: (rifa) {
          if (rifa == null) {
            return const Center(child: Text('Rifa no encontrada'));
          }
          final categoria = ref.watch(categoriaByIdProvider(rifa.categoriaId));
          if (categoria == null) {
            return const Center(child: Text('Categoría no encontrada'));
          }
          return _buildDetailView(context, ref, rifa, categoria);
        },
      ),
    );
  }

  Widget _buildDetailView(BuildContext context, WidgetRef ref, Rifa rifa, CategoriaRifa categoria) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Image/Color indicator
          Container(
            width: double.infinity,
            height: 100.0,
            decoration: BoxDecoration(
              color: _getColorFromString(categoria.color),
              borderRadius: BorderRadius.circular(8.0),
            ),
            child: Center(
              child: Text(
                categoria.nombre,
                style: const TextStyle(color: Colors.white, fontSize: 24.0, fontWeight: FontWeight.bold),
              ),
            ),
          ),
          const SizedBox(height: 16.0),
          // Description
          Text(
            'Descripción: ${rifa.nombre}',
            style: Theme.of(context).textTheme.headlineSmall,
          ),
          const SizedBox(height: 8.0),
          // Prize fund
          Text('Fondo de premios: \$${categoria.fondoPremios}'),
          const SizedBox(height: 8.0),
          // Prize per winner
          Text('Premio por ganador: \$${categoria.premioPorGanador}'),
          const SizedBox(height: 8.0),
          // Number of winners
          Text('Número de ganadores: ${rifa.numeroGanadores}'),
          const SizedBox(height: 8.0),
          // End date
          Text('Fecha de fin: ${rifa.fechaFin.toLocal().toString().split(' ')[0]}'),
          const SizedBox(height: 32.0),
          // Buy Ticket button
          ElevatedButton(
            onPressed: () => _showBuyTicketModal(context, ref, rifa.id),
            child: const Text('Comprar Boleto'),
          ),
        ],
      ),
    );
  }

  void _showBuyTicketModal(BuildContext context, WidgetRef ref, String rifaId) {
    int quantity = 1;

    showDialog(
      context: context,
      builder: (BuildContext context) {
        return StatefulBuilder(
          builder: (context, setState) {
            return AlertDialog(
              title: const Text('Comprar Boleto'),
              content: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Text('Selecciona la cantidad:'),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      IconButton(
                        onPressed: () {
                          if (quantity > 1) {
                            setState(() => quantity--);
                          }
                        },
                        icon: const Icon(Icons.remove),
                      ),
                      Text('$quantity'),
                      IconButton(
                        onPressed: () {
                          setState(() => quantity++);
                        },
                        icon: const Icon(Icons.add),
                      ),
                    ],
                  ),
                ],
              ),
              actions: [
                TextButton(
                  onPressed: () => Navigator.of(context).pop(),
                  child: const Text('Cancelar'),
                ),
                ElevatedButton(
                  onPressed: () async {
                    // Get payment intent from backend
                    final apiService = ref.read(apiServiceProvider);
                    const usuarioId = 'user-123'; // TODO: Get from auth
                    final paymentData = {
                      'rifaId': rifaId,
                      'usuarioId': usuarioId,
                      'cantidad': quantity,
                    };
                    try {
                      final response = await apiService.post('/api/v1/payments/create-intent', data: paymentData);
                      final clientSecret = response.data['clientSecret'];

                      // Present Stripe payment sheet
                      await Stripe.instance.initPaymentSheet(
                        paymentSheetParameters: SetupPaymentSheetParameters(
                          paymentIntentClientSecret: clientSecret,
                          merchantDisplayName: 'Rifa1122',
                        ),
                      );

                      await Stripe.instance.presentPaymentSheet();

                      // Confirm payment on backend
                      await apiService.post('/api/v1/payments/confirm', data: {'paymentIntentId': response.data['paymentIntentId']});

                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text('Pago completado exitosamente')),
                      );
                      Navigator.of(context).pop();
                    } catch (e) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text('Error: $e')),
                      );
                    }
                  },
                  child: const Text('Confirmar'),
                ),
              ],
            );
          },
        );
      },
    );
  }

  Color _getColorFromString(String colorName) {
    switch (colorName.toLowerCase()) {
      case 'gris':
        return Colors.grey;
      case 'marrón':
        return Colors.brown;
      case 'plata':
        return Colors.grey[400]!;
      case 'dorado':
        return Colors.amber;
      case 'verde':
        return Colors.green;
      case 'azul':
        return Colors.blue;
      case 'negro':
        return Colors.black;
      default:
        return Colors.grey;
    }
  }
}