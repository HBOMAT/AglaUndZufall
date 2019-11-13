
Bemerkungen für Programmierer/Entwickler
========================================

Zur Unterstützung der Fehlersuche ist im Hauptprogramm die Variable 
``_TEST`` vorgesehen, die im Quelltext geändert werden kann; bei 
``_TEST = True`` werden bei Fehlern die vollständigen Python-Fehlermeldungen 
angezeigt
	
Durch das *zufall*-Paket wird die Python-Sprache an einigen Stellen modifiziert
(Umdefinition der Operatoren '^' und '|', Unterbinden der Zuweisung eines Wertes 
an die Eigenschaft/Methode eines Objektes (``objekt.eigenschaft = wert``-
Konstrukt), Verwenden der deutschen Umlaute in Bezeichnern). Bei Änderungen 
oder Ergänzungen der *zufall*-Quelltexte dürfen diese Modifizierungen nicht
benutzt werden. Ebenso ist es nicht ratsam, innerhalb eines *zufall*-Notebooks
eine allgemeine Python-Programmierung durchzuführen
	
	
Aus der Sicht des Autors sollten die Schwerpunkte der weiteren Entwicklung 
des Paketes sein:
		
- Konfiguration der Jupyter-Oberfläche entsprechend den Bedürfnissen von 
  Lehrern und Schülern 
  
- Aufnahme weiterer statistischer Tests in das Paket

- Gestaltung der EreignisAlgebra-Klasse auf der Basis von logischen 
  Ausdrücken

- Bessere Verknüpfung der Dokumentation mit den Programmen	 

- Verbesserung der Fehlererkennung und -mitteilung	 

- Eventuelle Anpassung an das schnelle C++-Paket **SymEngine** (nach dessen 
  Fertigstellung durch die Entwickler; siehe `SymEngine`_)	

.. _SymEngine: https://pypi.org/project/symengine  









