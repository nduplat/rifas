import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

const Map<String, Color> categoriaColors = {
  'Hierro': Color(0xFF6D6D6D),
  'Bronce': Color(0xFFA97142),
  'Plata': Color(0xFFC0C0C0),
  'Oro': Color(0xFFFFD700),
  'Platino': Color(0xFFAFEEEE),
  'Esmeralda': Color(0xFF50C878),
  'Diamante': Color(0xFF1E90FF),
  'Maestro': Color(0xFF9370DB),
};

ThemeData appTheme = ThemeData(
  useMaterial3: true,
  fontFamily: GoogleFonts.poppins().fontFamily,
  textTheme: GoogleFonts.poppinsTextTheme(),
  cardTheme: const CardTheme(
    elevation: 4.0,
    margin: EdgeInsets.all(8.0),
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.all(Radius.circular(12.0)),
    ),
  ),
  colorScheme: const ColorScheme.light(
    primary: Color(0xFF1E90FF), // Diamante
    secondary: Color(0xFFFFD700), // Oro
    surface: Colors.white,
    background: Colors.white,
    error: Colors.red,
    onPrimary: Colors.white,
    onSecondary: Colors.black,
    onSurface: Colors.black,
    onBackground: Colors.black,
    onError: Colors.white,
  ),
);