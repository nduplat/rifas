import 'dart:convert';
import 'package:dio/dio.dart';

class MockApiService {
  final Dio _dio;

  MockApiService(this._dio);

  // Initial data for rifas
  final List<Map<String, dynamic>> _rifas = [
    {
      "id": "550e8400-e29b-41d4-a716-446655440003",
      "nombre": "Rifa Hierro",
      "categoriaId": "hierro-id",
      "loteriaId": "baloto-id",
      "fechaInicio": "2023-12-01T00:00:00.000Z",
      "fechaFin": "2023-12-24T23:59:59.000Z",
      "numeroGanadores": 1,
      "estado": "activa"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440004",
      "nombre": "Rifa Bronce",
      "categoriaId": "bronce-id",
      "loteriaId": "baloto-id",
      "fechaInicio": "2023-12-01T00:00:00.000Z",
      "fechaFin": "2023-12-24T23:59:59.000Z",
      "numeroGanadores": 1,
      "estado": "activa"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440005",
      "nombre": "Rifa Plata",
      "categoriaId": "plata-id",
      "loteriaId": "baloto-id",
      "fechaInicio": "2023-12-01T00:00:00.000Z",
      "fechaFin": "2023-12-24T23:59:59.000Z",
      "numeroGanadores": 1,
      "estado": "activa"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440006",
      "nombre": "Rifa Oro",
      "categoriaId": "oro-id",
      "loteriaId": "baloto-id",
      "fechaInicio": "2023-12-01T00:00:00.000Z",
      "fechaFin": "2023-12-24T23:59:59.000Z",
      "numeroGanadores": 1,
      "estado": "activa"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440007",
      "nombre": "Rifa Platino",
      "categoriaId": "platino-id",
      "loteriaId": "baloto-id",
      "fechaInicio": "2023-12-01T00:00:00.000Z",
      "fechaFin": "2023-12-24T23:59:59.000Z",
      "numeroGanadores": 1,
      "estado": "activa"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440008",
      "nombre": "Rifa Esmeralda",
      "categoriaId": "esmeralda-id",
      "loteriaId": "baloto-id",
      "fechaInicio": "2023-12-01T00:00:00.000Z",
      "fechaFin": "2023-12-24T23:59:59.000Z",
      "numeroGanadores": 1,
      "estado": "activa"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440009",
      "nombre": "Rifa Diamante",
      "categoriaId": "diamante-id",
      "loteriaId": "baloto-id",
      "fechaInicio": "2023-12-01T00:00:00.000Z",
      "fechaFin": "2023-12-24T23:59:59.000Z",
      "numeroGanadores": 1,
      "estado": "activa"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440010",
      "nombre": "Rifa Maestro",
      "categoriaId": "maestro-id",
      "loteriaId": "baloto-id",
      "fechaInicio": "2023-12-01T00:00:00.000Z",
      "fechaFin": "2023-12-24T23:59:59.000Z",
      "numeroGanadores": 1,
      "estado": "activa"
    },
  ];

  // Initial data for categorias
  final List<Map<String, dynamic>> _categorias = [
    {
      "id": "hierro-id",
      "nombre": "Hierro",
      "color": "Gris",
      "valorBoleta": 1000,
      "totalRecaudo": 100000,
      "rake": 0.1,
      "fondoPremios": 90000,
      "premioPorGanador": 90000,
    },
    {
      "id": "bronce-id",
      "nombre": "Bronce",
      "color": "Marrón",
      "valorBoleta": 5000,
      "totalRecaudo": 500000,
      "rake": 0.25,
      "fondoPremios": 375000,
      "premioPorGanador": 375000,
    },
    {
      "id": "plata-id",
      "nombre": "Plata",
      "color": "Plata",
      "valorBoleta": 10000,
      "totalRecaudo": 1000000,
      "rake": 0.3,
      "fondoPremios": 700000,
      "premioPorGanador": 700000,
    },
    {
      "id": "oro-id",
      "nombre": "Oro",
      "color": "Dorado",
      "valorBoleta": 25000,
      "totalRecaudo": 2500000,
      "rake": 0.35,
      "fondoPremios": 1625000,
      "premioPorGanador": 1625000,
    },
    {
      "id": "platino-id",
      "nombre": "Platino",
      "color": "Plata",
      "valorBoleta": 50000,
      "totalRecaudo": 5000000,
      "rake": 0.4,
      "fondoPremios": 3000000,
      "premioPorGanador": 3000000,
    },
    {
      "id": "esmeralda-id",
      "nombre": "Esmeralda",
      "color": "Verde",
      "valorBoleta": 100000,
      "totalRecaudo": 10000000,
      "rake": 0.45,
      "fondoPremios": 5500000,
      "premioPorGanador": 5500000,
    },
    {
      "id": "diamante-id",
      "nombre": "Diamante",
      "color": "Azul",
      "valorBoleta": 250000,
      "totalRecaudo": 25000000,
      "rake": 0.5,
      "fondoPremios": 12500000,
      "premioPorGanador": 12500000,
    },
    {
      "id": "maestro-id",
      "nombre": "Maestro",
      "color": "Negro",
      "valorBoleta": 500000,
      "totalRecaudo": 50000000,
      "rake": 0.55,
      "fondoPremios": 22500000,
      "premioPorGanador": 22500000,
    },
  ];

  // Initial data for loterias
  final List<Map<String, dynamic>> _loterias = [
    {
      "id": "baloto-id",
      "nombre": "Baloto",
      "descripcion": "Lotería nacional colombiana",
      "frecuencia": "semanal",
      "urlResultados": "https://www.baloto.com/resultados"
    },
  ];

  // Tickets storage
  final List<Map<String, dynamic>> _tickets = [];

  // GET /rifas
  Future<Response> getRifas() async {
    await Future.delayed(const Duration(milliseconds: 500)); // Simulate latency
    return Response(
      requestOptions: RequestOptions(path: '/rifas'),
      data: _rifas,
      statusCode: 200,
    );
  }

  // GET /categorias
  Future<Response> getCategorias() async {
    await Future.delayed(const Duration(milliseconds: 400)); // Simulate latency
    return Response(
      requestOptions: RequestOptions(path: '/categorias'),
      data: _categorias,
      statusCode: 200,
    );
  }

  // GET /rifas/{id}
  Future<Response> getRifaById(String id) async {
    await Future.delayed(const Duration(milliseconds: 300)); // Simulate latency
    final rifa = _rifas.firstWhere(
      (r) => r['id'] == id,
      orElse: () => null,
    );
    if (rifa == null) {
      return Response(
        requestOptions: RequestOptions(path: '/rifas/$id'),
        statusCode: 404,
        data: {'error': 'Rifa not found'},
      );
    }
    return Response(
      requestOptions: RequestOptions(path: '/rifas/$id'),
      data: rifa,
      statusCode: 200,
    );
  }

  // POST /tickets
  Future<Response> createTicket(Map<String, dynamic> ticketData) async {
    await Future.delayed(const Duration(milliseconds: 700)); // Simulate latency
    final rifaId = ticketData['rifaId'];
    final usedNumeros = _tickets.where((t) => t['rifaId'] == rifaId).map((t) => t['numero'] as int).toSet();
    int numero = -1;
    for (int i = 1; i <= 100; i++) {
      if (!usedNumeros.contains(i)) {
        numero = i;
        break;
      }
    }
    if (numero == -1) {
      return Response(
        requestOptions: RequestOptions(path: '/tickets'),
        statusCode: 400,
        data: {'error': 'No available ticket numbers'},
      );
    }
    final newTicket = {
      'id': 'ticket-${DateTime.now().millisecondsSinceEpoch}',
      'rifaId': rifaId,
      'usuarioId': ticketData['usuarioId'],
      'numero': numero,
      'compradoEn': DateTime.now().toIso8601String(),
      'estado': 'vendido',
  // GET /tickets?usuarioId={userId}
  Future<Response> getTicketsByUserId(String userId) async {
    await Future.delayed(const Duration(milliseconds: 500)); // Simulate latency
    final userTickets = _tickets.where((t) => t['usuarioId'] == userId).toList();
    return Response(
      requestOptions: RequestOptions(path: '/tickets'),
      data: userTickets,
      statusCode: 200,
    );
  }
    };
    _tickets.add(newTicket);
    return Response(
      requestOptions: RequestOptions(path: '/tickets'),
      data: newTicket,
      statusCode: 201,
    );
  }

  // GET /loterias
  Future<Response> getLoterias() async {
    await Future.delayed(const Duration(milliseconds: 400)); // Simulate latency
    return Response(
      requestOptions: RequestOptions(path: '/loterias'),
      data: _loterias,
      statusCode: 200,
    );
  }
}