
Lotto
=====

.. currentmodule:: zufall.lib.objekte.lotto

.. autoclass:: Lotto

   **Eigenschaften und Methoden**
   
   .. autoattribute:: hilfe
   
         Synonym: **h**   
         
   .. autoattribute:: formeln
   
   .. autoattribute:: gewinn
   
   .. autoattribute:: regeln
      
   .. autoattribute:: richtige
	  
   .. method:: spiel( /[ tipp ] /[, m ] ) )
   
         Spiel zur Simulation

         *tipp* : abgegebener Tipp (Liste mit 6 Zahlen aus {1, 2, ..., 49});  
         fehlt die Angabe, wird ein zufälliger Tipp angenommen	
		 
         *m* : Anzahl Spiele (mit dem gleichen Tipp); Standard=1
		 
         Zusatz:
            `z=ja` - Es wird ein zufälliger Tipp angenommen (ein eventuell
            angegebener Tipp wird nicht beachtet)
			
            `d=ja` - Bei Angabe von *m* > 1 Rückgabe einer DatenReihe 
            mit der Anzahl Richtige je Spiel
			
   |
   
   **Ausgewählte Eigenschaften und Methoden für die ZufallsGröße "Richtige"**			
			
      | richtige.erw	         
      | richtige.F(...)            
      | richtige.hist            
      | richtige.hist_kum        
      | richtige.n_omega         
      | richtige.omega           
      | richtige.P(...)            
      | richtige.sigma           
      | richtige.stich_probe(...)  
      | richtige.var             
      | richtige.versuch          
      | richtige.vert              
      | richtige.vert_kum         

   **Ausgewählte Eigenschaften und Methoden für die ZufallsGröße "Gewinn"**			
			
      | gewinn.erw              
      | gewinn.n_omega          
      | gewinn.omega            
      | gewinn.stich_probe(...)   
      | gewinn.versuch          
      | gewinn.vert             
      | gewinn.vert_kum        

   Bei einem Aufruf ist vor dem o.a. Namen die Lotto-Instanz zu notieren, etwa
   ``l.gewinn.erw``  

   Zu allen Eigenschaften und Methoden für eine ZufallsGröße siehe 
   :ref:`Seite für ZufallsGröße <spiele>`

   |

   **Synonyme Bezeichner**

      ``hist_kum     :  histKum``
   
      ``n_omega      :  nOmega``
   
      ``stich_probe  :  stichProbe``
   
      ``vert_kum     :  vertKum``
