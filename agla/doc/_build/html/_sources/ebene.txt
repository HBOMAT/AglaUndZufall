
Ebene
=====

.. currentmodule:: agla.lib.objekte.ebene

.. autoclass:: Ebene
   
   **Eigenschaften und Methoden**
   
   */statt* ``ue`` *kann* ``ü`` *geschrieben werden/*
   
   .. autoattribute:: hilfe
 	
   .. autoattribute:: aagl
      
   .. autoattribute:: dim
   
   .. autoattribute:: hnf
   
   .. autoattribute:: is_schar
   
   .. autoattribute:: koord
   
   .. method:: koord_(punkt)
   
         Auswertung der Koordinatengleichung in einem Punkt	
		 
         *punkt* : Punkt 		 

         Zusatz : `k=1` - Ausgabe der Koordinatengleichung       		 
		 
   .. autoattribute:: nf
   
   .. method:: nf_(punkt)
   
         Auswertung der Normalenform der Gleichung in einem Punkt	
		
         *punkt* : Punkt 		 
		
   .. autoattribute:: norm
   
   .. autoattribute:: par
   
   .. autoattribute:: prg
   
   .. method:: prg_(punkt)
           
         Auswertung der Parametergleichung in einem Punkt

         *punkt* : Punkt 		 
		 
   .. autoattribute:: punkte
   
   .. method:: punkte_()
   
         zu punkte zugehörig; Erläuterung der Ausgabe	  

   .. autoattribute:: richt
   
         Synonym: **spann**
      
   .. autoattribute:: sch_par
   
   .. autoattribute:: spur_xy

   .. autoattribute:: spur_xz
   
   .. autoattribute:: spur_yz
   
   .. autoattribute:: stuetz
   
         Synonym: **auf_pkt**   
   
   .. method:: abstand(objekt)   
   
         Abstand der Ebene zu einem anderen Objekt
      
         *objekt* : Punkt, Gerade, Ebene, Kugel
		 
         Zusatz : `d=n` - Dezimaldarstellung mit *n* Nachkomma-/Stellen
			
         Rückgabe :  0, wenn die Ebene *objekt* schneidet	
   
   .. method:: bild(abbildung)
   
         Bildebene bei einer Abbildung
		 
         *abbildung* : Abbildung des Raumes
   
   .. method:: parallele(punkt | abstand)

         Parallele Ebene durch einen gegebenen Punkt oder in einem 
         gegebenen Abstand		

         *punkt* :      Punkt
		 
         *abstand* :    Zahl; das Vorzeichen bestimmt die Lage
   
   .. method:: pkt(/[ wert1, wert2 ])
   
         Punkt der Ebene   
   
         *wert* : Wert eines Ebenenparameters

         Rückgabe :   
            bei Angabe von zwei Parameterwerten:
               Ebenenpunkt, der zu diesen Werten gehört
            bei leerer Argumentliste oder freien Bezeichnern:
               allgemeiner Punkt der Ebene 			

   .. method:: sch_el(wert)
   
         Element einer Ebenenschar mit einem Parameter
			
         *wert* : Wert des Scharparameters
		    
   .. method:: schnitt(objekt)
   
         Schnittmenge der Ebene mit einem anderen Objekt
		 
         *objekt* : Punkt, Gerade, Ebene, Kugel, Strecke
		 		 
         Zusatz: `l=1` - Lageinformationen
   
   .. method:: winkel(objekt)

         Winkel der Ebene mit einem anderen Objekt (in Grad)

         *objekt* : Vektor, Gerade, Ebene
		 		 
         Zusatz : `d=n` - Dezimaldarstellung mit *n* Nachkomma-/Stellen
   
|
   
   **Synonyme Bezeichner**

      ``hilfe       :  h``
	  
      ``auf_pkt     :  aufPkt``
	  
      ``is_schar    :  isSchar``
	  
      ``koord_      :  Koord``
	  
      ``nf_         :  Nf``
	  
      ``prg_        :  Prg``
	  
      ``punkte_     :  Punkte``
	  
      ``sch_el      :  schEl``
	  
      ``sch_par     :  schPar``
	  
      ``spur_xy     :  spurXY``
	  
      ``spur_xz     :  spurXZ``
	  
      ``spur_yz     :  spurYZ``

	  
