
Gerade
======

.. currentmodule:: agla.lib.objekte.gerade

.. autoclass:: Gerade
   	  	  
   **Eigenschaften und Methoden** für Geraden **in der Ebene**
	  
   .. autoattribute:: hilfe
   
   .. autoattribute:: aagl
   
   .. autoattribute:: anstieg
   
         Synonym: **m**   
      
   .. autoattribute:: dim
     
   .. autoattribute:: is_schar
   
   .. autoattribute:: fkt
   
   .. method:: fkt_(punkt)  

         Auswertung der Fuktionsgleichung in einem Punkt	   
   
   .. autoattribute:: hnf
   
   .. autoattribute:: koord
   
   .. method:: koord_(punkt)  
   
         Auswertung der Koordinatengleichung in einem Punkt	   
   
   .. autoattribute:: nf
   
   .. method:: nf_(punkt)  
   
         Auswertung der Normalenform der Gleichung in einem Punkt	      
   
   .. autoattribute:: norm
   
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
   
   .. autoattribute:: stuetz
   
         Synonym: **auf_pkt**   
   
   .. autoattribute:: y_abschn
	  
         Synonym: **n** 
	  
   .. method:: abstand(objekt)  
   
         Abstand der Geraden zu einem anderen Objekt
      		 
         *objekt* : Punkt, Gerade
		 
         Zusatz : `d=n` - Dezimaldarstellung mit *n* Nachkomma-/Stellen
			
         Rückgabe : 0, wenn die Gerade *objekt* schneidet	
   
   .. method:: bild(abbildung)
   
         Bildgerade bei einer Abbildung
		 
         *abbildung* : Abbildung der Ebene
   
   .. method:: normale(/[ punkt | wert ]) 
   
         Synonym: **senkrechte** 
   
         Normale in einem Geradenpunkt
		 
         *punkt* : Punkt der Geraden	
		 
         *wert* : Wert des Geradenparameters		 
		 
         Rückgabe :   
            bei Angabe eines Punktes oder Parameterwertes:
               Normale (im zugehörigen) Geradenpunkt
            bei leerer Argumentliste oder freiem Bezeichner:
               Normale im allgemeinen Geradenpunkt 			
		    
   .. method:: parallele(punkt | abstand)

         Parallele Gerade durch einen gegebenen Punkt oder in einem 
         gegebenen Abstand		

         *punkt* :      Punkt
		 
         *abstand* :    Zahl; das Vorzeichen bestimmt die Lage
   
   .. method:: pkt(/[wert])   
   
         Punkt der Geraden   
   
         *wert* : Wert des Geradenparameters

         Rückgabe :   
            bei Angabe eines Parameterwertes:
               Geradenenpunkt, der zu diesem Wert gehört	  
            bei leerer Argumentliste oder freiem Bezeichner:
               allgemeiner Punkt der Geraden 			
   
   .. method:: sch_el(wert) 
   
         Element einer Geradenschar mit einem Parameter
   	 
         *wert* : Wert des Scharparameters
		    
   .. method:: schnitt(objekt)
   
         Schnittmenge der Geraden mit einem anderen Objekt
		 
         *objekt* : Punkt, Gerade, Strecke, Kreis
		 		 
         Zusatz: `l=1` - Lageinformationen
   
   .. method:: winkel(objekt)

         Winkel der Geraden mit einem anderen Objekt (in Grad)

         *objekt* : Vektor, Gerade
		 		 
         Zusatz : `d=n` - Dezimaldarstellung mit *n* Nachkomma-/Stellen
	 
|
   
   **Synonyme Bezeichner in der Ebene**
   
      ``hilfe     :  h``
	  	  
      ``auf_pkt   :  aufPkt``
	  
      ``gleich_   :  Gleich``
	  
      ``is_schar  :  isSchar``
	  
      ``fkt_      :  Fkt``
	  
      ``koord_    :  Koord``
	  
      ``nf_       :  Nf``
	  	  
      ``prg_      :  Prg``
	  
      ``punkte_   :  Punkte``
	  
      ``sch_el    :  schEl``
	  
      ``sch_par   :  schPar``
	  
      ``y_abschn  :  yAbschn``
	  
   
