# LV-PY-WaterBottleMeter
Wizualizacja procesu "water bottle meter" zrealizowana w LabVIEW i Python. Aplikacja zapisuje wyniki pomiarów do lokalnej bazy danych.

# Opis instalacji
Do poprawnego działania aplikacji wymagane są:
1. LabVIEW w wersji 2024 Q3 lub nowszej
2. Python w wersji 3.10.x
3. Lokalnie utworzona baza danych, zalecany PostgreSQL jako SZDB (System Zarządzania Bazą Danych)

Po instalacji, należy umieścić pliki z gałęzi "main" w jednym folderze. Aplikację należy uruchamiać dwuklikiem na plik Main.vi, a nie przez launcher LabVIEW. W innym przypadku skrypt Pythona nie jest w stanie otworzyć pliku ze zdjęciem zbiornika (np. water.jpg).

Aby wykorzystać lokalną bazę danych, należy utworzyć źródło danych ODBC (Open Database Connectivity) typu "PostgreSQL ODBC Driver(ANSI)", który przechowa informacje dotyczące sposobu nawiązania połączenia ze wskazaną bazą danych. Zalecana nazwa źródła danych to "PostgreSQL30". Jeśli użytkownik życzy sobie ustawić inną niż zalecana, konieczna jest modyfikacja "Connection string" w klastrze "DB info", w stanie "Data: Initialize", w pliku Main.vi.

Finalnie, należy w systemowych ustawieniach kamery zezwolić na używanie jej przez wiele aplikacji w tym samym czasie. Brak zezwolenia będzie wiązał się z brakiem możliwości akwizycji obrazu z kamery przez skrypt Pythona.
