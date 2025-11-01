import 'package:rifa1122/features/rifas/models/rifa.dart';
import 'package:rifa1122/features/rifas/models/categoria_rifa.dart';

class AIRecommenderService {
  final List<Rifa> allRifas;
  final List<CategoriaRifa> allCategorias;

  AIRecommenderService(this.allRifas, this.allCategorias);

  List<Rifa> recomendarRifas(List<Rifa> historial) {
    // Create a map for quick categoria lookup
    final Map<String, CategoriaRifa> categoriaMap = {
      for (var categoria in allCategorias) categoria.id: categoria
    };

    // Count frequency of categorias in historial
    final Map<String, int> categoriaFrequency = {};
    for (var rifa in historial) {
      categoriaFrequency[rifa.categoriaId] = (categoriaFrequency[rifa.categoriaId] ?? 0) + 1;
    }

    // Calculate average valor_boleta from historial
    final double averageValorBoleta = historial.isEmpty
        ? 0.0
        : historial
            .map((rifa) => categoriaMap[rifa.categoriaId]!.valorBoleta)
            .reduce((a, b) => a + b) /
            historial.length;

    // Filter active rifas, excluding those already in historial
    final List<Rifa> activeRifas = allRifas
        .where((rifa) =>
            rifa.estado == 'activa' &&
            !historial.any((h) => h.id == rifa.id))
        .toList();

    // Calculate similarity score for each active rifa
    double calculateScore(Rifa rifa) {
      final int freq = categoriaFrequency[rifa.categoriaId] ?? 0;
      final int valor = categoriaMap[rifa.categoriaId]!.valorBoleta;
      final double valorSimilarity = averageValorBoleta == 0
          ? 0.0
          : 1 / (1 + (valor - averageValorBoleta).abs() / averageValorBoleta);
      return freq + valorSimilarity;
    }

    // Sort by score descending and take top 5
    activeRifas.sort((a, b) => calculateScore(b).compareTo(calculateScore(a)));
    return activeRifas.take(5).toList();
  }
}