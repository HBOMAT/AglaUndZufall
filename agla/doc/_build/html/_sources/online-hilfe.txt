
Online - Hilfe
==============

Das Paket *agla* verfügt über ein eigenes Hilfesysten, sodass in einer
Jupytersitzung jederzeit entsprechende Informationen erhalten werden können

Unter dem Namen ``Hilfe`` steht eine Funktion zur Verfügung, über die zentrale
Hilfeinformationen erfügbar sind. Mit der Eingabe

.. code-block:: python

   In [..]: Hilfe()     # oder Hilfe(h=1)
   
in eine Code-Zelle des Notebooks wird man auf einzelne Seiten geleitet (der  
erste Teil ``In [..]:`` wird von Jupyter selbst erzeugt, die vorgenommene 
Nummerierung entspricht der Reihenfolge, in der die Zellen ausgeführt 
wurden)

Weitere Hilfeinformationen können zu jedem *agla*-Objekt und zu den Methoden
eines Objektes gewonnen werden, indem bei der Erzeugung des Objektes mit 
Hilfe seiner Erzeugerfunktion oder beim Aufruf der Methode als letzter (oder
einziger) Eintrag in der Argumentenliste `h=1` geschrieben wird. Man erhält 
dann unmittelbar die gewünschte Information oder wird auf eine andere 
Hilfeseite geleitet

.. code-block:: python

   In [..]: Ebene(h=1)   # Hilfe über die Erzeugerfunktion

   In [..]: # Hilfe für eine Methode
            e = Ebene(1, 3, -2, 4)   # ein Objekt (Ebene-Instanz)
            e.schnitt(h=1)           # und seine Methode  
   
Analoges gilt für die Funktionen, die von *agla* zur Verfügung gestellt werden

Weiterhin ist für jedes Objekt eine Eigenschaft mit dem Namen ``h`` (Kurzform 
von ``hilfe``) vorhanden, bei deren Aufruf die für dieses Objekt verfügbaren 
Eigenschaften und Methoden aufgelistet werden

.. code-block:: python

   In [..]: e.h   # Hilfe für ein Objekt mit dem Namen e    

Tritt in einer Syntaxdarstellung die Konstruktion ``/[...]`` auf, kann die
Angabe zwischen den eckigen Klammern entfallen. Ein ``|``-Zeichen bedeutet im 	
Allgemeinen, dass zwischen zwei Angaben ausgewählt werden kann

|

   