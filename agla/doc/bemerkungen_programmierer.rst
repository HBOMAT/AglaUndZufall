
Bemerkungen für Programmierer/Entwickler
========================================

Zur Unterstützung der Fehlersuche ist im Hauptprogramm die Variable 
``_TEST`` vorgesehen, die im Quelltext geändert werden kann; bei 
``_TEST = True`` werden bei Fehlern die vollständigen Python-Fehlermeldungen 
angezeigt
	
Durch das *agla*-Paket wird die Python-Sprache an einigen Stellen modifiziert
(Umdefinition der Operatoren '^' und '|', Unterbinden der Zuweisung eines Wertes 
an die Eigenschaft/Methode eines Objektes (``objekt.eigenschaft = wert``-
Konstrukt), Verwenden der deutschen Umlaute in Bezeichnern). Bei Änderungen 
oder Ergänzungen der *agla*-Quelltexte dürfen diese Modifizierungen nicht
benutzt werden. Ebenso ist es nicht ratsam, innerhalb eines *agla*-Notebooks
eine allgemeine Python-Programmierung durchzuführen
	
Aus der Sicht des Autors sollten die Schwerpunkte der weiteren Entwicklung 
des Paketes sein:
		
- Konfiguration der Jupyter-Oberfläche entsprechend den Bedürfnissen von 
  Lehrern und Schülern
  
- Verwendung eines Parsers  
	 
- Verbesserung der Fehlermeldungen für die Benutzer
	 
- Konsequente Nutzung der OOP, speziell bei den Grafik-Routinen
   
- Einsatz von **VisPy** für 3D nach Vorliegen einer stabilen Version
  Die entsprechenden Grafik-Methoden sind zu entwickeln; ihre 
  Aktivierung erfolgt im Quelltext mittels der grafik_3d-Methode des 
  Umgebung-Objektes; siehe `VisPy`_ 
	 
- Animationsfähigkeit aller 3D- und 2D-Objekte (einschließlich 
  sphärische und hyperbolische Geometrie) mittels VisPy		
	 
- Bessere Verknüpfung der Dokumentation mit den Programmen	 

- Verbesserung der Fehlererkennung und -mitteilung	 
	 
- Einbinden des schnellen C++-Paketes **SymEngine**; an einer Stelle
  (Modul hyp_geometrie) ist SymEngine-Code enthalten, der aktuell 
  lediglich Probezwecken dient; siehe `SymEngine`_	

.. _VisPy: https://vispy.org  
.. _SymEngine: https://pypi.org/project/symengine  









