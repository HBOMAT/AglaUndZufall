.. _link:

3D-Grafiken (Mayavi)
====================

Grafiken werden mittels der Anweisung::

   In [..]: Grafik(...)   # oder
   
   In [..]: zeichne(...) 
   
hergestellt. Siehe dazu :ref:`Grafik-Funktion <Grafik>` und 
:ref:`Grafik-Spezifikationen <grafik_spezifikationen>`

Das Zeitverhalten ist bei einigen Grafiken nicht akzeptabel. Das wird sich
durch den vorgesehenen Einsatz von **VisPy** (ein schnelles Python-
Grafikprogramm) sowie des schnellen **CAS SymEngine** (es ist in C++  
geschrieben und hat eine SymPy/Python-Anbindung) mittelfristig ändern. Beide			  
Pakete befinden sich seit 2012 bzw. 2013 in der Entwicklung

| 

Bemerkungen zu **Windows**-Anwendungen

Es kann immer nur eine Grafik (in einem eigenen Fenster) offen sein.
Ist eine Grafik offen, werden unter der entsprechenden Zelle des Notebooks
liegende Zellen erst dann ausgeführt, wenn das Fenster mit der Grafik 
geschlossen wurde

Tastatur- und Maus-Bedienung einer Grafik:

``Linke-Maus-Taste`` gedrückt lassen und ziehen - Drehen der Kamera	

zusätzlich ``Umsch-Taste`` gedrückt lassen - Verschieben der Grafik
	
zusätzlich ``Strg-Taste`` gedrückt lassen - Drehen der Grafik um die 
Kameraachse		

zusätzlich ``Umsch+Strg-Tasten`` gedrückt lassen - Ein-/Auszoomen
 	
``Rechte-Maus-Taste`` gedrückt lassen und ziehen - Ein-/Auszoomen
 		
``Mittlere-Maus-Taste`` gedrückt lassen und ziehen - Verschieben der Grafik	

``Mausrad drehen``- Ein-/Auszoomen der Grafik 		

|
