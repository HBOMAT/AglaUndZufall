
Zugriff auf Eigenschaften und Methoden
======================================

Die *agla*-Objekte haben verschiedene Eigenschaften und Methoden (die 
letzteren erwarten für ihre Ausführung Argumente - ein weiteres Objekt, einen 
Parameterwert o.ä.). Die implementierten Eigenschaften und Methoden eines
Objektes können z.B. über die Hilfeseite seiner Klasse, etwa mit

.. code-block:: python

   In [..]: Gerade(h=1)   # führt auf h=2 bzw. h=3

ermittelt werden. Ein Gerade-Objekt ``g`` hat z.B. die Eigenschaft 
``richt`` (Richtungsvektor) und die Methode ``abstand`` (Abstand zu einem 
anderen Objekt). Der Zugriff erfolgt mittels des ``.`` - Operators, der 
allgemein in der Objektorientierten Programmierung Verwendung findet. Sei 
z.B. ``e`` eine Ebene, so kann der Zugriff auf die genannte Eigenschaft und 
die genannte Methode mit den Anweisungen 

.. code-block:: python

   In [..]: g.richt   

   In [..]: g.abstand( e ) 
   
erfolgen
		
Der Zugriff auf eine Methode wird generell über einen Funktionsaufruf 
realisiert, der Argumente erwartet, die voneinander durch ``,`` getrennt und 
in Klammern eingeschlossen werden. Hier wurde das Argument ``e`` 
angegeben, es soll der Abstand der Geraden ``g`` zur Ebene ``e`` ermittelt 
werden

Zu einigen Eigenschaften existiert eine Methode mit gleichem Namen, der auf 
einen Unterstrich ``_`` endet. Damit besteht die Möglichkeit, mittels des 
entsprechenden Funktionsaufrufes zusätzliche Informationen/Leistungen
anzufordern. Welche das sind, kann über die Hilfeanforderung (`h=1` als 
letzter Eintrag in der Argumentliste) erfahren werden. Diese zu Eigenschaften 
gehörenden Methoden können auch über den Namen der Eigenschaft mit großem 
Anfangsbuchstaben aufgerufen werden, also z.B. für die Eigenschaft ``prg`` 
von ``g``

.. code-block:: python

   In [..]: g.prg_(...)    # oder   

   In [..]: g.Prg(...) 
   
		
Das Ergebnis eines Eigenschafts-/Methodenaufrufes kann ein Tupel oder eine
Liste sein, etwa die beiden Richtungsvektoren einer Ebene ``e``, die mit

.. code-block:: python

   In [..]: e.richt   

erhalten werden. Um auf ein einzelnes Element zuzugreifen, wird der 
Indexzugriff verwendet	

.. code-block:: python

   In [..]: e.richt[0]   # bzw.
   In [..]: e.richt[1]
   
Zu beachten ist, dass die Zählung gemäß der Python-Konvention bei 0 beginnt		
   
|
   