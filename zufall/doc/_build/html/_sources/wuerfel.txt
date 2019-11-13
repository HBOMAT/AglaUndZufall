
Würfel
======

.. currentmodule:: zufall.lib.objekte.wuerfel

.. autoclass:: Wuerfel
   
   **Eigenschaften und Methoden**
   
   */statt* ``ae`` *kann* ``ä`` *geschrieben werden/*
   
   .. autoattribute:: hilfe
   
         Synonym: **h**   
   
   .. autoattribute:: anzahl

   .. autoattribute:: erw
   
   .. method:: erw_()
   
         Erwartungswert; zugehörige Methode
		 
         Zusatz: `d=n`   Darstellung dezimal mit *n* Kommastellen		 
		 
   .. autoattribute:: flaechen
      
   .. autoattribute:: graf_F
   
   .. autoattribute:: hist
   
   .. method:: hist_()
   
         Histogramm; zugehörige Methode

         Zusatz: 
            `p=ja``  Polygonzug-Diagramm	

            Angabe einer Zufallsgröße / Datenreihe - Vergleich mit anderer 
            Verteilung			
		 
   .. autoattribute:: hist_kum
   
   .. autoattribute:: n_omega
   
   .. autoattribute:: omega
   
   .. autoattribute:: poly_zug
   
   .. method:: poly_zug_()
   
         Polygonzug; zugehörige Methode
		 
         Zusatz: 
            `hi=ja``  Histogramm	

            Angabe einer Zufallsgröße / Datenreihe - Vergleich mit anderer 
            Verteilung			
		 
   .. autoattribute:: sigma
   
   .. method:: sigma_()
   
         Standardabweichung; zugehörige Methode

         Zusatz: `d=n`  Darstellung dezimal mit *n* Kommastellen	
		 
   .. autoattribute:: var
   
   .. method:: var_()
   
         Varianz; zugehörige Methode

         Zusatz: 
            `d=n`  Darstellung dezimal mit *n* Kommastellen	

            `b=ja` Begriffe		
		 
   .. autoattribute:: versuch
   
   .. autoattribute:: vert
   
   .. method:: vert_()
   
         Wahrscheinlichkeitsverteilung; zugehörige Methode

         Zusatz: 
            `p=ja` Wahrscheinlichkeiten werden als Prozentwerte ausgegeben	

            `d=n` ebenso, dezimal mit *n* Kommastellen		
		 
            `s=ja` Spaltenausgabe	

            `sp=ja` ebenso, Prozentwerte	

            `sd=n` ebenso, dezimal mit *n* Kommastellen		
					 
   .. autoattribute:: vert_kum
   
   .. method:: vert_kum_()
   
         Kumulierte Wahrscheinlichkeitsverteilung; zugehörige Methode

         Zusatz: 
            `p=ja` Wahrscheinlichkeiten werden als Prozentwerte ausgegeben	

            `d=n` ebenso, dezimal mit *n* Kommastellen		
		 
            `s=ja` Spaltenausgabe	

            `sp=ja` ebenso, Prozentwerte	

            `sd=n` ebenso, dezimal mit *n* Kommastellen						 		 

   .. method:: F(wert)
   
         Verteilungsfunktion
		 		 
         *wert* : Zahl

         Zusatz: `d=n` - Darstellung dezimal mit *n* Kommastellen		 

   .. method:: P(e, /[e1] )
       
         Wahrscheinlichkeit eines Ereignisses   
   
         *e*: Ereignis
		 
            | *elem* |
            | *Liste/Tupel/Menge* von Elementen der Ergebnismenge |
            | *X = elem* |
            | *elem rel X* |
            | *X rel elem* | 
            | *abs( X - elem ) rel zahl* |
            | *'elem rel X rel elem'*  (Zeichenkette)
            | der Bezeichner *X* ist zwingend
			
         *e1* :  *elem* | *Liste/Tupel/Menge* von Elementen der Ergebnismenge
		 
         *elem* :   Element der Ergebnismenge
		 
         *rel* : Relation  < | <= | > | >=
		 
         *zahl* : reelle Zahl
		 
         Bei der Angabe von zwei Ereignissen wird die bedingte Wahrscheinlichkeit
         :math:`P( e | e_1 )` berechnet			

         Zusatz:
            `p=ja` - Darstellung als Prozentwert
			
            `d=n` - Darstellung dezimal mit *n* Kommastellen
			
            `g=ja` - grafische Darstellung			
		 		 
   .. method:: quantil(q)
   
         Quantile
		 
         *q* : Zahl aus [0,1]  
		 
   .. method:: relh2p(e, m)
   
         Stabilisierung der relativen Häufigkeiten
		 
         *e*: Ereignis
		 
            *Element* | *Liste* | *Tupel* | *Menge* von Elementen der 
            Ergebnismenge 
			  
         *m*: Anzahl Versuche
		 
   .. method:: stich_probe(m)
   	  
         Stichprobe

         *m* : Umfang (Anzahl Versuche)

         Zusatz: `d=ja` - Rückgabe als DatenReihe		 
   
   |

   **Synonyme Bezeichner**
   		
        ``erw_        :  Erw``
		
        ``graf_F      :  grafF``
    	
        ``hist_       :  Hist``
	
        ``hist_kum    :  histKum``
		
        ``n_omega     :  nOmega``
		
        ``poly_zug    :  polyZug``
   
        ``poly_zug_   :  PolyZug``
		
        ``sigma_      :  Sigma``
   
        ``stich_probe :  stichProbe``
		
        ``var_        :  Var``
   
        ``vert_       :  Vert``
		
        ``vert_kum    :  vertKum``
   
        ``vert_kum_   :  VertKum``
		
   