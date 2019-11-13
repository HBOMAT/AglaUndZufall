
Craps
=====

.. currentmodule:: zufall.lib.objekte.craps

.. autoclass:: Craps

   **Eigenschaften und Methoden**
   
   .. autoattribute:: hilfe
   
         Synonym: **h**   
         
   .. autoattribute:: formeln
   
   .. autoattribute:: regeln
      
   .. method:: spiel( /[, m] )
   
         Spiel

         *m* : Anzahl Spiele; Standard=1
		 
         Zusatz:
            `g=ja` - Grafik des Gewinn-Verlaufes
			
            `d=ja` - Grafik des Verlaufes der mittleren Spieldauer
			
            `dr=ja` - Bei Angabe von *m* > 1 Rückgabe von zwei DatenReihen
			
               | - mit 1 (Gewinn) oder -1 (Verlust) je Spiel *und*
               | - mit der Spieldauer je Spiel
			   
            `gdr=ja` - Gewinnverlauf + DatenReihen
			
            `ddr=ja` - ebenso mittlere Dauer
