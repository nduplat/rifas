import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:shimmer/shimmer.dart';
import 'package:rifa1122/features/rifas/data/rifas_repository.dart';
import 'package:rifa1122/features/rifas/models/rifa.dart';
import 'package:rifa1122/features/rifas/models/categoria_rifa.dart';
import 'package:rifa1122/features/ai_recommender/data/ai_recommender_service.dart';

// Provider for fetching rifas
final rifasProvider = FutureProvider<List<Rifa>>((ref) async {
  final rifasRepo = ref.watch(rifasRepositoryProvider);
  return rifasRepo.getRifas();
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

// Provider for AI recommender service
final aiRecommenderProvider = Provider<AIRecommenderService>((ref) {
  final rifasAsync = ref.watch(rifasProvider);
  final categoriasAsync = ref.watch(categoriasProvider);

  return rifasAsync.maybeWhen(
    data: (rifas) => categoriasAsync.maybeWhen(
      data: (categorias) => AIRecommenderService(rifas, categorias),
      orElse: () => AIRecommenderService([], []),
    ),
    orElse: () => AIRecommenderService([], []),
  );
});

// Provider for recommended rifas (mock user history)
final recommendedRifasProvider = FutureProvider<List<Rifa>>((ref) async {
  final aiRecommender = ref.watch(aiRecommenderProvider);
  // Mock user history - in real app this would come from user data
  final mockHistory = <Rifa>[];
  return aiRecommender.recomendarRifas(mockHistory);
});

class RifaListScreen extends ConsumerWidget {
  const RifaListScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final rifasAsync = ref.watch(rifasProvider);
    final recommendedAsync = ref.watch(recommendedRifasProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Rifas'),
      ),
      body: rifasAsync.when(
        loading: () => _buildShimmerList(),
        error: (error, stack) => Center(child: Text('Error: $error')),
        data: (rifas) => _buildRifaListWithRecommendations(context, ref, rifas, recommendedAsync),
      ),
    );
  }

  Widget _buildShimmerList() {
    return ListView.builder(
      itemCount: 8,
      itemBuilder: (context, index) {
        return Shimmer.fromColors(
          baseColor: Colors.grey[300]!,
          highlightColor: Colors.grey[100]!,
          child: Card(
            margin: const EdgeInsets.all(8.0),
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Container(
                    width: double.infinity,
                    height: 20.0,
                    color: Colors.white,
                  ),
                  const SizedBox(height: 8.0),
                  Container(
                    width: 100.0,
                    height: 16.0,
                    color: Colors.white,
                  ),
                  const SizedBox(height: 8.0),
                  Container(
                    width: 80.0,
                    height: 16.0,
                    color: Colors.white,
                  ),
                  const SizedBox(height: 8.0),
                  Container(
                    width: 120.0,
                    height: 16.0,
                    color: Colors.white,
                  ),
                  const SizedBox(height: 16.0),
                  Container(
                    width: 100.0,
                    height: 36.0,
                    color: Colors.white,
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }

  Widget _buildRifaListWithRecommendations(BuildContext context, WidgetRef ref, List<Rifa> rifas, AsyncValue<List<Rifa>> recommendedAsync) {
    return ListView(
      children: [
        // Recommended section
        recommendedAsync.when(
          loading: () => const SizedBox.shrink(),
          error: (error, stack) => const SizedBox.shrink(),
          data: (recommended) => recommended.isNotEmpty ? _buildRecommendedSection(context, ref, recommended) : const SizedBox.shrink(),
        ),
        // All rifas section
        _buildAllRifasSection(context, ref, rifas),
      ],
    );
  }

  Widget _buildRecommendedSection(BuildContext context, WidgetRef ref, List<Rifa> recommended) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.all(16.0),
          child: Text(
            'Recomendadas para ti',
            style: Theme.of(context).textTheme.headlineSmall,
          ),
        ),
        SizedBox(
          height: 200.0,
          child: ListView.builder(
            scrollDirection: Axis.horizontal,
            itemCount: recommended.length,
            itemBuilder: (context, index) {
              final rifa = recommended[index];
              final categoria = ref.watch(categoriaByIdProvider(rifa.categoriaId));

              if (categoria == null) {
                return const SizedBox.shrink();
              }

              return Container(
                width: 160.0,
                margin: const EdgeInsets.only(left: 16.0, right: index == recommended.length - 1 ? 16.0 : 0.0),
                child: Card(
                  child: Padding(
                    padding: const EdgeInsets.all(12.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Container(
                          width: 20.0,
                          height: 20.0,
                          decoration: BoxDecoration(
                            color: _getColorFromString(categoria.color),
                            shape: BoxShape.circle,
                          ),
                        ),
                        const SizedBox(height: 8.0),
                        Text(
                          rifa.nombre,
                          style: Theme.of(context).textTheme.titleMedium,
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                        ),
                        const SizedBox(height: 4.0),
                        Text('\$${categoria.valorBoleta}'),
                        const Spacer(),
                        ElevatedButton(
                          onPressed: () {
                            context.go('/rifa/${rifa.id}');
                          },
                          child: const Text('Ver'),
                        ),
                      ],
                    ),
                  ),
                ),
              );
            },
          ),
        ),
      ],
    );
  }

  Widget _buildAllRifasSection(BuildContext context, WidgetRef ref, List<Rifa> rifas) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.all(16.0),
          child: Text(
            'Todas las rifas',
            style: Theme.of(context).textTheme.headlineSmall,
          ),
        ),
        ListView.builder(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          itemCount: rifas.length,
          itemBuilder: (context, index) {
            final rifa = rifas[index];
            final categoria = ref.watch(categoriaByIdProvider(rifa.categoriaId));

            if (categoria == null) {
              return const SizedBox.shrink(); // Or handle missing categoria
            }

            return Card(
              margin: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 4.0),
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Category color indicator
                    Container(
                      width: 24.0,
                      height: 24.0,
                      decoration: BoxDecoration(
                        color: _getColorFromString(categoria.color),
                        shape: BoxShape.circle,
                      ),
                    ),
                    const SizedBox(height: 8.0),
                    Text(
                      rifa.nombre,
                      style: Theme.of(context).textTheme.headlineSmall,
                    ),
                    const SizedBox(height: 4.0),
                    Text('Valor del boleto: \$${categoria.valorBoleta}'),
                    const SizedBox(height: 4.0),
                    Text('Fecha fin: ${rifa.fechaFin.toLocal().toString().split(' ')[0]}'),
                    const SizedBox(height: 16.0),
                    ElevatedButton(
                      onPressed: () {
                        context.go('/rifa/${rifa.id}');
                      },
                      child: const Text('Ver detalles'),
                    ),
                  ],
                ),
              ),
            );
          },
        ),
      ],
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