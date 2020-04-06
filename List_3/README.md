Krótka instrukcja:
I. Moduł archive.py:

1. Przy korzystaniu z tego modułu najpierw należy podać parametr --mode. W zależności co chcemy zrobić. (archive, unarchive, backup, change_endlines)
2. 

a) Jeśli korzystamy z trybu archive musimy podać argumenty  '--archive_paths' (minimum 2 ścieżki)
Najpierw ścieżki do plików które chcemy zarchwiziować (lub plik) a jako ostatni argument ściężkę do archwium. Uwaga ścieżka do archwium nie powinna jeszcze istnieć.

b) Jeśli korzystamy z trybu unarchive musimy podać argumenty --unarchive_paths (dokładnie 2 ścięzki)
Najpierw ścieżkę do istniejącego archiwum, a następnie ściężkę do folderu, gdzie pliki mają zostać "wypakowane".

c) Jeśli korzystamy z trybu backup musimy podać argument --backup_paths (1 ścieżkę ) oraz --format (dowolna ilość)
Argumentem --backup_paths powinna być ścieżka do folderu, z którego pliki chcemy poddać backupowi. Natomiast argumentami format mogą być: "txt" "pdf" "jpg" itd.
Uwaga. w module archive możemy zmienić wartość zmiennej 'windows' w zależności z jakiego systemu korzystamy. Jeśli korzystamy z innych systemów jak windows nalezy zmienić jej wartość na 'False'.


d) Jeśli korzystamy z trybu change_endlines musimy podać dodtkowo argument do --unix_to_wind lub --wind_to_unix w zależności jakiej transformacji chcemy dokonać. W powyższych zmiennych powinniśmy podać ścieżkę do folderu, z którego wszystkie pliki tekstowe powinny zostać poddane transformacji bądź do wybranego pliku tekstowego, jeśli chcemy dokonać transformacji jedynie w jednym pliku.


W folderze Tests zostały przygotowane przykładowe pliki aby sprawdzić działanie programu.