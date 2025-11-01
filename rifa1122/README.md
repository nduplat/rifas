# Rifa1122

A Flutter application for managing raffles (rifas).

## Setup Instructions

### 1. Install Dependencies
Run the following command to install all required dependencies:
```
flutter pub get
```

### 2. Generate Code
This project uses Freezed for code generation. Run the build runner to generate the necessary files:
```
flutter pub run build_runner build
```

### 3. Execute the App
To run the application on a connected device or emulator:
```
flutter run
```

## Additional Notes
- Ensure you have Flutter SDK installed and configured.
- For iOS development, you may need to run `pod install` in the `ios` directory after `flutter pub get`.
- The app uses mock API services for demonstration purposes.
