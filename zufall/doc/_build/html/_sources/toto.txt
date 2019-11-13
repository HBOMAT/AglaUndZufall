
Toto - FussballToto
===================

.. currentmodule:: zufall.lib.objekte.toto

.. autoclass:: FussballToto

   **Eigenschaften und Methoden**
   
   .. autoattribute:: hilfe
   
         Synonym: **h**   
         
   .. autoattribute:: formeln
   
   .. autoattribute:: regeln
      
   .. autoattribute:: richtige
	  
   .. method:: spiel( /[ tipp ] /[, m ] ) )
   
         Spiel zur Simulation; 7 statt 11 Mannschaften

         *tipp* : abgegebener Tipp (Liste mit 7 Zahlen aus {0, 1, 2}); fehlt 
         die Angabe, wird ein zufälliger Tipp angenommen	
		 
         *m* : Anzahl Spiele (mit dem gleichen Tipp); Standard=1
		 
         Zusatz:
            `z=ja` - Es wird ein zufälliger Tipp angenommen (ein eventuell
            angegebener Tipp wird nicht beachtet)
			
            `d=ja` - Bei Angabe von *m* > 1 Rückgabe einer DatenReihe 
            mit der Anzahl Richtige je Spiel
			
Eigenschaften und Methoden für die ZufallsGröße "Richtige" siehe 
:ref:`Seite für ZufallsGröße <spiele>`