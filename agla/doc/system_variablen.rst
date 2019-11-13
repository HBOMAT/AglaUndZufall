
System - Variablen
==================

System-Variablen können vom Benutzer mittels  der Zuweisung von ``True`` bzw. ``False`` gesetzt werden. 
Die Einstellungen wirken global in seiner Arbeitsumgebung während einer *agla*-Sitzung und können 
beliebig oft verändert werden

``UMG.SIMPL`` - zur Vereinfachung bei der Erzeugung von Vektoren (Umwandlung von ``float``-Komponenten in rationale Zahlen)

    Voreinstellung: ``UMG.SIMPL = True``
	
``UMG.EXAKT`` - zur exakten Berechnung hyperbolischer Objekte

    Voreinstellung: ``UMG.EXAKT = False``
	
(``UMG`` ist ein Objekt der Klasse ``Umgebung``)	
	
Weiterhin existiert die System-Variable ``_TEST`` (Voreinstellung: ``False``). Sie kann nur im Quelltext 
des Start-Programmes (durch den Programmierer) verändert werden. Bei ``_TEST = True`` werden bei auftretenden 
Fehlern die vollständigen Python-Fehlermeldungen angezeigt 