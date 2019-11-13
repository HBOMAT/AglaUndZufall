
Online - Hilfe
==============

Das Paket *zufall* verfügt über ein eigenes Hilfesysten, sodass in einer
Jupytersitzung jederzeit entsprechende Informationen erhalten werden können

Unter dem Namen ``Hilfe`` steht eine Funktion zur Verfügung, über die zentrale
Hilfeinformationen erfügbar sind. Mit der Eingabe

.. code-block:: python

   In [..]: Hilfe()     # oder Hilfe(h=1)
   
in eine Code-Zelle des Notebooks wird man auf einzelne Seiten geleitet (der  
erste Teil ``In [..]:`` wird von Jupyter selbst erzeugt, die vorgenommene 
Nummerierung entspricht der Reihenfolge, in der die Zellen ausgeführt 
wurden)

Weitere Hilfeinformationen können zu jedem *zufall*-Objekt und zu den Methoden
eines Objektes gewonnen werden, indem bei der Erzeugung des Objektes mit 
Hilfe seiner Erzeugerfunktion oder beim Aufruf der Methode als letzter (oder
einziger) Eintrag in der Argumentenliste `h=1` geschrieben wird. Man erhält 
dann unmittelbar die gewünschte Information oder wird auf eine andere 
Hilfeseite geleitet

.. code-block:: python

   In [..]: BV(h=1)   # Hilfe über die Erzeugerfunktion; BV ist der Kurzname
                      # für die BinomialVerteilung-Klasse
					  
   In [..]: # Hilfe für eine Methode
            bv = BV(24, 1/4)   # ein Objekt (BV-Instanz)
            bv.P(h=1)          # und seine Methode (Berechnung von Wahrsch.) 
   
Analoges gilt für die Funktionen, die von *zufall* zur Verfügung gestellt werden

Weiterhin ist für jedes Objekt eine Eigenschaft mit dem Namen ``h`` (Kurzform 
von ``hilfe``) vorhanden, bei deren Aufruf die für dieses Objekt verfügbaren 
Eigenschaften und Methoden aufgelistet werden

.. code-block:: python

   In [..]: bv.h   # Hilfe für ein Objekt mit dem Namen bv     

Tritt in einer Syntaxdarstellung die Konstruktion ``/[...]`` auf, kann die
Angabe zwischen den eckigen Klammern entfallen. Ein ``|``-Zeichen bedeutet im 	
Allgemeinen, dass zwischen zwei Angaben ausgewählt werden kann

|

   