
Gerade
======

.. currentmodule:: agla.lib.objekte.gerade

.. autoclass:: Gerade
   
   **Eigenschaften und Methoden** für Geraden **im Raum**

   */statt* ``ue`` *kann* ``ü`` *geschrieben werden/*
   
   .. autoattribute:: hilfe
 	   
   .. autoattribute:: dim
   
   .. autoattribute:: is_schar
   
   .. autoattribute:: par
   
   .. autoattribute:: prg
   
         Synonym: **gleich**
		 
   .. method:: prg_(punkt) 
   
         Auswertung der Parametergleichung in einem Punkt	

         Synonym: **gleich_**
		   
   .. autoattribute:: punkte
   
   .. method:: punkte_()   
   
         zu punkte zugehörig; Erläuterung der Ausgabe	     
   
   .. autoattribute:: richt
   
   .. autoattribute:: sch_par

   .. autoattribute:: spur_xy
   
   .. autoattribute:: spur_xz

   .. autoattribute:: spur_yz
	
   .. autoattribute:: stuetz
   
         Synonym: **auf_pkt**   

   .. method:: abstand(objekt)  
   
         Abstand der Geraden zu einem anderen Objekt
      
         *objekt* : Punkt, Gerade, Ebene, Kugel
		 		 
         Zusatz : `d=n` - mit *n* Nachkomma-/Stellen)
			
         Rückgabe : 0, wenn die Gerade *objekt* schneidet	
      
   .. method:: bild(abbildung)   
   
         Bildgerade bei einer Abbildung
		 
         *abbildung* : Abbildung
   
   .. method:: pkt(/[wert])   
   
         Punkt der Geraden   
   
         *wert* : Wert des Geradenparameters

         Rückgabe :   
            bei Angabe eines Parameterwertes:
               Geradenenpunkt, der zu diesem Wert gehört
					  
            bei leerer Argumentliste oder freiem Bezeichner:
               allgemeiner Punkt der Geraden 			
   
   .. method:: proj(ebene)
   
         Projektion der Geraden auf eine Ebene

         *ebene*: Ebene; Koordinatenebene oder zu einer von diesen 
         parallele Ebene		 
   
   .. method:: sch_el(wert)  
   
         Element einer Geradenschar mit einem Parameter
			
         *wert* : Wert des Scharparameters   
   
   .. method:: schnitt(objekt) 

         Schnittmenge der Geraden mit einem anderen Objekt
		 
         *objekt* : Punkt, Gerade, Ebene, Kugel, Strecke, Dreieck, Viereck
		 		 				 
         Zusatz: `l=1` - Lageinformationen
      
   .. method:: winkel(objekt)   

         Winkel der Geraden mit einem anderen Objekt (in Grad)

         *objekt* : Vektor, Gerade, Ebene
		 		 		 
         Zusatz : `d=n` - Dezimaldarstellung mit  *n* Nachkomma-/Stellen  
	  	  
|
   
   **Synonyme Bezeichner im Raum**

      ``hilfe       :  h``
	  
      ``auf_pkt     :  aufPkt``
	  
      ``gleich_     :  Gleich``
	  
      ``is_schar    :  isSchar``
	  	  
      ``prg_        :  Prg``
	  
      ``punkte_     :  Punkte``
	  
      ``sch_el      :  schEl``
	  
      ``sch_par     :  schPar``
	  
      ``spur_xy     :  spurXY``
	  
      ``spur_xz     :  spurXZ``
	  
      ``spur_yz     :  spurYZ``	  
	  	  
|