## LV-PY-WaterBottleMeter
Wizualizacja procesu "water bottle meter" zrealizowana w LabVIEW i Python. Aplikacja zapisuje wyniki pomiarów do lokalnej bazy danych.

### Opis instalacji
Do poprawnego działania aplikacji wymagane są:
1. LabVIEW w wersji 2024 Q3 lub nowszej.
2. Python w wersji 3.10.x (LabVIEW wspiera natywnie wersje od 3.6.x do 3.10.x; chęć użycia innej wersji wymaga zmiany "Python version" w klastrze "Python info", w stanie "Data: Initialize").
3. Lokalnie utworzona baza danych (zalecany PostgreSQL jako SZBD (System Zarządzania Bazą Danych), po instalacji należy pamiętać o zainstalowaniu sterownika psqlODBC chociażby przy użyciu Stack Buildera).

Po instalacji, należy umieścić pliki z gałęzi "main" w jednym folderze. Po wykonaniu tej czynności możliwe jest otworzenie projektu z poziomu launchera LabVIEW lub poprzez dwuklik na plik .lvproj. **Zalecane jest jednak otwieranie bezpośrednio pliku Main.vi, ponieważ w innym przypadku skrypt Pythona może nie być w stanie odczytać pliku zdjęcia.**

Aby wykorzystać lokalną bazę danych, należy utworzyć źródło danych ODBC (Open Database Connectivity), wykorzystujące sterownik "PostgreSQL ODBC Driver(ANSI)", które przechowa informacje dotyczące sposobu nawiązania połączenia ze wskazaną bazą danych. Zalecana nazwa źródła danych to "PostgreSQL30". Jeśli użytkownik życzy sobie ustawić inną niż zalecana, konieczna jest modyfikacja "Connection string" w klastrze "DB info", w stanie "Data: Initialize".

Finalnie, należy w systemowych ustawieniach kamery zezwolić na używanie jej przez wiele aplikacji w tym samym czasie. Brak zezwolenia będzie wiązał się z brakiem możliwości akwizycji obrazu z kamery przez skrypt Pythona.
