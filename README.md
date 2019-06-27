Bardzo proste skrypty służace aby zescrapować rożne dane ze `spanishdict.com` i trochę z Wikisłownika.

## Ogóny Zarys Modelu Probabilistycznego 

To będzie polegać na tym, że empirycznie oblicznymy empiryczne prawdopodobieństwo/częstotliwość każdego słowa z `esp.dict` w korpusie przykładów (lub przymiemy liczby zapisany w źródle).  

Wtedy każdemu przykładowi przypisujemy przypisujemy empiryczne prawdopodobieństwo pojawienie się zdania na podstawie prostego Markowskiego modelu tworzenia zdań. Stała kontynuowania zdania gamma będzie umowna.  

Znormalizujemy wynikające liczby o prawdopodobieństwo że losowe zdanie jest w korpusie przykładów. Innymi słowy, dzielimy przez sumę prawdopodobieństw wszystkich zdań.  

Próbkujemy powstającą dystrybucję, tworząc porządek na korpusie która faworyzuje najbardziej naturalne przykłady (pod względem częstotliwości występowania występujących w nich słów)  

Pobieramy głosy Joanny i Mia z AWS Polly.  

Z uporządkowanego zestawu ang/esp/głosy robimy talię Anki..  

## Możliwe Ulepszenia - Problemy

Powinienem rowikłać kwestie kognatów w słowniku.

Przykłady i słowa powinny być powiązane: jeśli dane przykład zostaje pomyślnie zrobiony, to powinno wpłynąć korzystnie na ocenę wszystkich występujących w nim słów. Natomiast, gdy spaprę jakieś zdanie, to muszę wytyczyć sposób określenia że to a nie inne słowo mnie wadziło.

Musi być jakas synchronizacja między praktyką odbywającym się na komórce a komputerem. Plan jest taki by słuchać angielskie,  a potem z repetycją hiszpańskie spacerując z komórki, robić normalną praktykę anki na komputerze

a co jeśli dystrybucja nie będzie tak jaką przewidziałem? Na przykład, może być że długość wyrazu zdominuje prawdopodobieństwo, a utkwimy w bagnie krótkawych przykładów. Albo że poszczególne odmiany koniugacji czasowników będą mocna karane przez system mimo że mogą być odmianyniezbędnego słowa. A przecież koniugacji należy się ćwiczyć...
