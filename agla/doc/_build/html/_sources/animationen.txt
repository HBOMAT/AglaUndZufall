
Animationen
===========

Animationen sind gegenwärtig nur in 3D möglich (mit Mayavi), sie befinden   		
sich in einem experimentellen Stadium

Animierte Grafiken sind für folgende Klassen im Raum implementiert:
	
- Vektor (nur Punktdarstellung)
- Gerade
- Ebene
- Kugel
- Strecke
- Dreieck
- Viereck                                             
- Kreis 
- Kegel
- Zylinder		  
- Körper
- Pyramide
- Prisma		  
- Kurve			                       
- Fläche 
	
Es kann nur ein Parameter (je Objekt) animiert werden. Generell nicht 
animierbar sind Pfeile und gefüllte Objekte sowie die Grenzen eines 
Parameterbereiches. Weitere Einschränkungen sind, dass Kurven nicht 
verfeinert bzw. als Röhre animiert dargestellt und Flächen nicht mit 
Gitternetz oder als Drahtdarstellung animiert werden  können. Des weiteren
ist die Bedienung zum Ablaufen einer Animation provisorisch

Eine Animation wird erzeugt, indem innerhalb einer ``zeichne/Grafik``
-Anweisung in der Spezifikation des zu animierenden Objektes eine Angabe 
zum Parameter in der Form::

   ( /[name, ] unten, oben /[, anzahl] )
	
gemacht wird. Hier sind ``name`` der Parametername (er kann auch weggelassen 
werden), ``unten`` und ``oben`` die untere und obere Grenze des 
Parameterbereiches und ``anzahl`` die Anzahl der Unterteilungen desselben 
(bei Weglassen wird der Standardwert 20 angenommen). Ein Beispiel ist::

   In [..]: f = Fläche(...)  # mit einem Parameter
   
   In [..]: zeichne( [ f, gelb, (-3, 3, 200) ] 
   
Das synchrone Ablaufen bei der gleichzeitigen Animation mehrerer Objekte
erfordert die Übereinstimmung der Angaben zu ``unten``, ``oben`` und
``anzahl``

Bei der Ausführung öffnen sich zwei Fenster - für die eigentliche Grafik und
ein kleines Bedienfenster, in dem zunächst der ``Delay``-Eintrag von 
Interesse ist. Der dort enthaltene große Wert garantiert genügend Zeit, um 
die beiden Fenster in eine günstige Position zu rücken. Die eigentliche 
Animation wird gestartet, indem dieser Wert verringert wird. Dazu wird der 
Cursor mit der Maus am Ende des ``Delay``-Feldes platziert. Dann können 
mit der Rücktaste genügend Ziffern gelöscht werden. Eine laufende Animation 
kann mit den entsprechenden Schaltern gestoppt und wieder gestartet werden. 
Die Grafik kann jederzeit verschoben, gedreht und gezoomt werden
	
Bemerkung zur Arbeit mit Windows: Die Ausführung von weiter unten liegenden 
Zellen des Notebooks ist erst möglich, wenn beide Fenster wieder geschlossen 
wurden

|
