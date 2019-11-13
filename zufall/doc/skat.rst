
Skat - SkatBlatt
================

.. currentmodule:: zufall.lib.objekte.skat_blatt

.. autoclass:: SkatBlatt

   **Eigenschaften und Methoden**
     
   .. autoattribute:: hilfe
   
         Synonym: **h**   
         
   .. autoattribute:: omega
   
         Synonym: **blatt**   
         
   .. method:: P( e /[, e1] )
   
         Wahrscheinlichkeit eines Ereignisses beim einmaligen Ziehen 
         einer Karte
  
         *e* : Ereignis
 
             | *einzelne Karte* | *Menge/Liste/Tupel* von Karten |          

             | *Ereignis* beim Ziehen einer Karte (siehe unten)
			 
         Bei der Angabe von zwei Ereignissen wird die bedingte 
         Wahrscheinlichkeit :math:`P( e | e_1 )` berechnet
			
   