Autor: Michał Sagan,                                  Krakow, 28.06.2021
========================================================================

* Zawartosc:
============

Katalog line_follower zawiera dwa katalogi z plikami:
--------------------------------------------------------------------

I.  Katalog worlds zawiera pliki: world1.wbt, world2.wbt, world3.wbt.
	Format .wbt wywodzi się z języka VRML97 i jest czytelny dla człowieka.
	W plikach tych znajdują się wszystkie ustawienia i parametry symulacji.
	Każdy plik odpowiada za inną symulację

II. Katalog controlers zawiera podkatalogi: LineFollower oraz LineFollowerNR,
	które z kolei zawierają skrypty z rozszerzeniem .py o tych samych nazwach.
	Kontrolery to programy, które sterują zachowaniem robota podczas symulacji.

------------------------------------------------------------------------
Reszta katalogów zostałą wygenerowana automatycznie przez środowisko 
Webots i jest pusta.

* Jak uruchomic sybulację:
=========================

Aby uruchomić symulację należy:
1) Pobrać oraz zainstalować język Python https://python.org/downloads.
2) Pobrać oraz zainstalować Webots https://cyberbotics.com
3) Otworzyć w programie Webots jeden z plików z rozszerzeniem .wbt
4) Upewnić się, że symulacja jest wstrzymana, a wirtualny czas, który upłynął, wynosi 0. 
Jeśli tak nie jest, zresetować symulację za pomocą panelu sterowania w górnej części ekranu
5) W drzewie sceny (po prawej stronie) wybrać węzeł:
e-puck -> controller -> Sellect... natępnie należy wybrać odpowiedni 
kontroler (LineFollowerNR lub LineFollower).
6) Uruchomić symulację naciskając przycisk 'Run the simulation in the real time'.

========================================================================



