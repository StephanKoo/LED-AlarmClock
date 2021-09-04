# Planung Funktionalität

## v0.2

* [x] Uhr automatisch beim Start des Rasperry Pi starten
* [x] Programm mit kill sauber beenden können
* [x] Die IP-Adresse wird jede Minute auf dem Display ausgegeben (Entwicklungs-Feature)

## v0.3

* [X] Abdunklung der LEDs, damit es nachts nicht so hell ist.
 * offen: Die Anwesenheit der Abdunklung als Erkennung für Tag-/Nacht-Modus nutzen.
* [ ] Ohne Lüfter laufen lassen, aber mindestens warnen und am Besten sinnvoll reagieren, wenn die CPU zu warm wird
* [ ] Knöpfe anschließen, um den Wecker damit auszuschalten
* [ ] den Rasperry Pi per Knopf runterfahren können (`sudo poweroff`)

## v0.4

* [ ] Wecken können, Weckzeitpunkte aus dem Dateisystem laden können
* [ ] die nächste Weckzeit per Knopfdruck auf dem Display ausgeben können.

## v0.5

* [ ] die bisher jede Minute angezeigten Informationen per Knopfdruck gezielt anfordern können, Zuordnung von Knopf zu Funktion erstmal hart kodiert

## v0.6

* [ ] flexibel konfigurierbare Menüs, um die einzelnen Informationen abzufragen
* [ ] Menüpunkte mit kleiner Schrift und/oder als Icons darstellen (das ist aussagekräftiger als ein Buchstabe)

## v0.7

* [ ] BVG-Abfrage mit der Ausgabe der Abfahtszeiten der Buslinien

## xN.N

* [ ] für den Wecker die erste relevante Zeit einstellen können (z.B. "7:30 Frühstück" oder "9:00 M37" (=Abfahrt mit dem Bus M37)). Das Gerät erkennt anhand der Konfiguration für "Früstück" und "M37", wann dann der Wecker klingeln muss.
* [ ] Weckzeiten per Knöpfe einstellen können
* [ ] Weckzeiten per http einstellen und kontrollieren können.
* [ ] Programm soll beim sudo poweroff sauber beenden. Hier soll systemd helfen. Noch rausfinden, wie.

# Version 3 oder so

* [ ] Erkennung, dass man noch im Bett liegt, und dann intensiv weiterwecken, sonst aber nicht
