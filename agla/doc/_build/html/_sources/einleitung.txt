
Einleitung
==========

**agla** ist das Ergebnis der Übertragung des gleichnamigen **MuPAD**-Paketes 
in die Programmiersprache **Python**. Hauptsächliches Ziel war es,  
kommerzielle Abhängigkeiten auszuzschalten und freie Software zu benutzen  

Hinsichtlich der Funktionalität wurde eine 1-zu-1-Übertragung angestrebt, 
die für Anwendungen in der Schule (entsprechend den heutigen Lehrplänen) 
weitgehend erreicht wurde

Python ist ein sehr guter konventioneller Taschenrechner. Durch das 
**CAS SymPy** werden seine Fähigkeiten vor allem um das symbolische Rechnen 
erweitert, mit *agla* (**A**\ nalytische **G**\ eometrie und 
**L**\ ineare **A**\ lgebra) ist eine Erweiterung auf das Feld des 
geometrischen Rechnens gegeben. Es ist vor allem für den Gebrauch in der 
Schule vorgesehen
	
In *agla* werden die geometrischen Objekte Vektor, Gerade, Ebene usw. mit  	
entsprechenden Python-**Klassen** dargestellt. Über eine Konstruktor-/
Erzeuger-funktion gleichen Namens können Instanzen dieser Klassen (Objekte), 
erzeugt
werden. Mit diesen und ihren Eigenschaften und Methoden wird dann interaktiv 
gearbeitet. Neben den Klassen zur euklidischen Geometrie werden auch einige 	
Klassen zur sphärischen und zur hyperbolischen Geometrie bereitgestellt. 
Weiterhin unterstützen einige **Funktionen** die Arbeit
		
Das Paket basiert auf dem vollständig in Python geschriebenen CAS SymPy und
ist selbst ebenfalls (mit leichten Modifizierungen) in reinem Python 
geschrieben. Für 2D-Grafiken wird das **matplotlib**-Paket benutzt, für 3D
**Mayavi**. Zukünftig soll das in der Entwicklung befindliche **VisPy** zur 
Anwendung kommen
		
Als Python-Paket wird *agla* innerhalb von **Jupyter**-Notebooks mit
englischer Bedienoberfläche benutzt

Die Syntax zur Handhabung des Paketes ist so gestaltet, dass sie leicht  
erlernbar ist. Es sind nur geringe Python-Kenntnisse sowie Fähigkeiten zur  
Arbeit mit einem Jupyter-Notebook erforderlich
 
Bei der Nutzung von *agla* kann auf den gesamten Leistungsumfang von Python 
zugegriffen werden, der vor allem duch eine Vielzahl weiterer Pakete 
realisiert wird	
   
Die Programme von *agla* werden im Quellcode kostenlos für die Benutzung 
bereitgestellt 

Die Pakete `SymPy`_, `Jupyter`_, `matplotlib`_, `Mayavi`_ und (zukünftig) 
`VisPy`_ liegen als freie Software ebenfalls im (Python-) Quellcode vor
   
.. _SymPy: https://www.sympy.org 

.. _Jupyter: http://jupyter.org   


.. _matplotlib: https://matplotlib.org   

.. _Mayavi: https://docs.enthought.com/mayavi/mayavi   

.. _VisPy: http://vispy.org 
  
|

