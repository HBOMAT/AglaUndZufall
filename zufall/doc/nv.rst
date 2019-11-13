
NV - NormalVerteilung
=====================


.. currentmodule:: zufall.lib.objekte.normal_verteilung

.. autoclass:: NormalVerteilung
   
   **Eigenschaften und Methoden**
   
   .. autoattribute:: hilfe
   
         Synonym: **h**   
      
   .. autoattribute:: erw
   
         Synonym: **mu**      
   
   .. method:: erw_()
   
        Erwartungswert; zugehörige Methode  

        Zusatz: `d=n` Darstellung dezimal mit *n* Kommastellen		
      
   .. autoattribute:: formeln
      
   .. autoattribute:: graf_D
   
   .. autoattribute:: graf_F
   
   .. autoattribute:: sigma
   
   .. method:: sigma_()
   
         Standardabweichung; zugehörige Methode

         Zusatz: `d=n` - Darstellung dezimal mit *n* Kommastellen		 
      
   .. autoattribute:: var
   
   .. method:: var_()
   
         Varianz; zugehörige Methode

         Zusatz: 
            `d=n` - Darstellung dezimal mit *n* Kommastellen	

            `b=ja` - Begriffe			
   
   .. autoattribute:: versuch
   			   
   .. method:: dichte(x)
   
         Dichtefunktion

         *x* : Zahl		 
   
         Zusatz: `d=n` - Darstellung dezimal mit *n* Kommastellen		 
   
   .. method:: F(x)
   
         Verteilungsfunktion

         *x* : Zahl
		 
         Zusatz: `d=n` - Darstellung dezimal mit *n* Kommastellen		 
   
   .. method:: P( e )
       
         Wahrscheinlichkeit eines Ereignisses   
   
         *e*: Ereignis
		 
            | *X rel zahl* | 
            | *zahl rel X* |
            | *abs( X - zahl ) rel zahl* |
            | *'zahl rel X rel zahl'*  (Zeichenkette)
            | der Bezeichner *X* ist zwingend
			
         *rel* : Relation  < | <= | > | >=
		 
         *zahl* : reelle Zahl
		 
         Zusatz:
            `p=ja` - Darstellung als Prozentwert
			
            `d=n` - Darstellung dezimal mit *n* Kommastellen
			
            `g=ja` - grafische Darstellung					 
   
   .. method:: quantil(q)
   
         Quantile
		 
         *q* : Zahl aus [0,1]  
      
   .. method:: stich_probe(m)
  
         Stichprobe   
  
         *m* : Umfang (Anzahl Versuche)  

         Zusatz: `d=ja` - Rückgabe als DatenReihe		 
		 
|

   **Synonyme Bezeichner**
   		
        ``erw_         :  Erw``
   	
        ``graf_F       :  graf_F``
		
        ``graf_D       :  graf_D``
	   
        ``sigma_       :  Sigma``
	
        ``stich_probe  :  stichProbe``
		
        ``var_         :  Var``
	
