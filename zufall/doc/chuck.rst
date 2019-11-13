
Chuck - ChuckALuck
==================

.. currentmodule:: zufall.lib.objekte.chuck

.. autoclass:: ChuckALuck

   **Eigenschaften und Methoden**
   
   .. autoattribute:: hilfe
   
         Synonym: **h**   
         
   .. autoattribute:: formeln
   
   .. autoattribute:: regeln
   

   .. autoattribute:: gewinn
   
   .. method:: spiel( /[zahl /[, m] )
   
         Spiel
		 
         *zahl* :
		 
            | genannte Zahl aus {0, 1, 2, 3, 4, 5, 6}
            | fehlt die Angabe, wird eine zufällige Zahl angenommen

         *m* : Anzahl Spiele (mit der selben Zahl); Standard=1
		 
         Zusatz:
            `z=ja` - Es wird eine zufällige Zahl angenommen; eine eventuell
            angegebene Zahl wird nicht beachtet
			
            `d=ja` - Bei Angabe von *m* > 1 Rückgabe einer DatenReihe mit 
            dem Gewinn pro Spiel

Eigenschaften und Methoden für die ZufallsGröße "Gewinn" siehe 
:ref:`Seite für ZufallsGröße <spiele>`
 
 
