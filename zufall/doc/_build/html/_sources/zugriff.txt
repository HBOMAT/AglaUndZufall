
Zugriff auf Eigenschaften und Methoden
======================================

Die *zufall*-Objekte haben verschiedene Eigenschaften und Methoden (die 
letzteren erwarten für ihre Ausführung Argumente - ein weiteres Objekt, einen 
Parameterwert o.ä.). Die implementierten Eigenschaften und Methoden eines
Objektes können z.B. über die Hilfeseite seiner Klasse, etwa mit

.. code-block:: python

   In [..]: BV(h=1)   # führt auf h=3

ermittelt werden. Eine BinomialVerteilung-Instanz ``bv`` hat z.B. die 
Eigenschaft ``vert`` (Wahrscheinlichkeitsverteilung) und die Methode ``P`` 
(zur Berechnung von Wahrscheinlichkeiten). Der Zugriff erfolgt mittels des ``.`` 
- Operators, der allgemein in der Objektorientierten Programmierung 
Verwendung findet. Sei  

.. code-block:: python

   In [..]: bv = BV(20, 1/5)   

so kann der Zugriff auf die genannte Eigenschaft und die genannte Methode mit
den Anweisungen 

.. code-block:: python

   In [..]: bv.vert   # die Verteilung (als dict/dictionary)

   In [..]: bv.P( X < 12 )   # die Wahrscheinlichkeit für Trefferanzahl 
                             # kleiner 12
   
erfolgen
		
Der Zugriff auf eine Methode wird generell über einen Funktionsaufruf 
realisiert, der Argumente erwartet, die in Klammern einzuschließen sind. Hier 
ist das einzige Argument der Vergleichsausdrck ``X < 12`` angegeben, der
das Ereignis "Die Anzahl der Treffer ist kleiner als 12" beschreibt. Sind  
mehrere Argumente anzugeben, sind sie durch Komma zu trennen 

Zu einigen Eigenschaften existiert eine Methode mit gleichem Namen, der auf 
einen Unterstrich ``_`` endet. Damit besteht die Möglichkeit, mittels des 
entsprechenden Funktionsaufrufes zusätzliche Informationen/Leistungen
anzufordern. Welche das sind, kann über die Hilfeanforderung (`h=1` als 
letzter Eintrag in der Argumentliste) erfahren werden. Diese zu Eigenschaften 
gehörenden Methoden können auch über den Namen der Eigenschaft mit großem 
Anfangsbuchstaben aufgerufen werden, also z.B. für die Eigenschaft ``vert_`` 
von ``bv``

.. code-block:: python

   In [..]: bv.vert_(...)    # oder   

   In [..]: bv.Vert(...) 
   
Das Ergebnis eines Eigenschafts-/Methodenaufrufes kann ein dictionary sein,
etwa die Wahrscheinlichkeitsverteilung ``bv.vert``. Auf ein einzelnes 
Argument kann mit dem Schlüssel zugegriffen werden, etwa mit

.. code-block:: python

   In [..]: bv.vert[5]
   
Auf einzelne Elemente von Tupeln oder Listen kann mittels Index bzw. darauf 
basierendem Ausdruck zugegriffen werden, etwa auf einzelne Elemente einer 
DatenReihe (Kurzform DR)

.. code-block:: python

   In [..]: dr = DR([7, 3, 3, 5, 8])

   In [..]: dr.daten[:3]  # eine Liste mit den ersten drei Datenelementen 
   
Zu beachten ist, dass die Zählung gemäß der Python-Konvention bei 0 beginnt		
   
|
   