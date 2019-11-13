
ZE - ZufallsExperiment
======================

.. currentmodule:: zufall.lib.objekte.zufalls_experiment

.. autoclass:: ZufallsExperiment
   
   **Eigenschaften und Methoden**
   
   .. autoattribute:: hilfe
   
         Synonym: **h**   
   
   .. autoattribute:: anordn
  
   .. autoattribute:: baum
   
   .. method:: baum_()
  
         Baumdiagramm; zugehörige Methode
		 
         Zusatz :    
            `p=ja` - Wahrscheinlichkeiten werden als Prozentwerte ausgegeben
			
            `d=n` - Wahrscheinlichkeiten werden als Dezimalzahlen mit *n* 
               Kommastellen ausgegeben		 
      
   .. autoattribute:: n_omega
      
   .. autoattribute:: omega

   .. method:: omega_()
   
         Ergebismenge; zugehörige Methode

         Zusatz :    
            `l=ja` - Listenausgabe
			
            `t=ja` - Tabellenausgabe		 

            `g=ja` - Größe der Ergebnismenge		 
			
   .. autoattribute:: stufen
   
   .. autoattribute:: versuch
   
         Synonyme: **ausfall**, **wurf**, **ziehen**

   .. autoattribute:: vert
   
   .. method:: vert_()
   
         Wahrscheinlichkeitsverteilung

         Zusatz :    
            `p=ja` - Wahrscheinlichkeiten werden als Prozentwerte ausgegeben
			
            `d=n` - ebenso, dezimal mit *n* Kommastellen		 

            `s=ja` - Spaltenausgabe		 
			
            `sp=ja` - ebenso, Prozentwerte		 

            `sd=n` - ebenso, dezimal mit *n* Kommastellen

   .. autoattribute:: wiederh
   
   .. method:: P(e /[, e1])
   
         Wahrscheinlichkeit eines Ereignisses

         *e*: Ereignis
		 
            *Element* | *Liste* | *Tupel* | *Menge* von Elementen der 
            Ergebnismenge 

         Bei der Angabe von zwei Ereignissen wird die bedingte 
         Wahrscheinlichkeit :math:`P( e | e_1 )` berechnet

         Zusatz:		 
            `p=ja` - Darstellung als Prozentwert
			
            `d=n` - Darstellung dezimal mit *n* Kommastellen		 
			
   .. method:: relh2p(e, m)
   
         Stabilisierung der relativen Häufigkeiten
		 
         *e*: Ereignis
		 
            *Element* | *Liste* | *Tupel* | *Menge* von Elementen der 
            Ergebnismenge 
			  
         *m*: Anzahl Versuche
		 
         Zusatz:  `d=ja`  
            | Rückgabe einer DatenReihe mit den Versuchsausgängen
            | 1 - Ereignis ist eingetreten
            | 0 - Ereignis ist nicht eingetreten
	 		
   .. method:: stich_probe(m)
   
         Stichprobe   
  
         *m* : Umfang (Anzahl Versuche)   
		 
         Zusatz: `l=ja` - Darstellung der Versuchsausgänge als Liste	 		 
   
   |

   **Synonyme Bezeichner**
   		
        ``baum_       :  Baum``
	
        ``n_omega     :  nOmega``
   
        ``omega_      :  Omega``
	
        ``stich_probe :  stichProbe``

        ``vert_       :  Vert``
		
        