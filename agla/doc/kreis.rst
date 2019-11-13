
Kreis
=====

.. currentmodule:: agla.lib.objekte.kreis

.. autoclass:: Kreis
   
   **Eigenschaften und Methoden**

   */statt* ``ae`` *kann* ``ä`` *geschrieben werden/*
   
   .. autoattribute:: hilfe
   
         Synonym: **h**   

   .. autoattribute:: dim
   
   .. autoattribute:: ebene
   
   .. autoattribute:: flaeche
   
   .. method:: flaeche_()
   
         Flächeninhalt; Dezimaldarstellung
		 
         Zusatz : 
            `d=n` - mit *n* Nachkomma-/Stellen
			
            `f=1` - Formel		 
   
   .. autoattribute:: gleich
   
   .. method:: gleich_(punkt)
   
         Auswertung der Gleichung in einem Punkt; nur in der Ebene	      
   
   .. autoattribute:: in_kurve
   
   .. autoattribute:: is_schar
         
   .. autoattribute:: mitte
   
         Synonyme: **M**, **m**
   
   .. autoattribute:: prg
   
   .. autoattribute:: radius
   
         Synonym: **r**
   
   .. method:: radius_()
   
         Radius; Dezimaldarstellung
		 
         Synonym: **r_**
   
         Zusatz : `d=n` - mit *n* Nachkomma-/Stellen   	    	 
      
   .. autoattribute:: sch_par
   
   .. autoattribute:: umfang
   
         Synonym: **laenge**
   
   .. method:: umfang_()

         Umfang; Dezimaldarstellung
		 
         Synonym: **laenge_**
		 
         Zusatz : 
            `d=n` - mit *n* Nachkomma-/Stellen   	    	 
      
            `f=1` - Formel		 
	  
   .. method:: bild(abbildung)
   
         Bildkreis bei einer Abbildung
		 
         *abbildung* : Abbildung
   
   .. method:: bogen(par_unt, par_ob)
 
         Kreisbogen
		 
         *par_unt* : untere Bereichsgrenze des Kreisparameters (in Grad)
		 
         *par_ob* : ebenso, obere Grenze   
   
   .. method:: pkt(/[wert] )   
   
         Punkt des Kreises   
   
         *wert* : Wert des Kreisparameters

         Rückgabe :   
            bei Angabe eines Parameterwertes:
               Kreispunkt, der zu diesem Wert gehört
					  
            bei leerer Argumentliste oder freiem Bezeichner:
               allgemeiner Punkt des Kreises 			
   
   .. method:: sch_el(wert) 
   
         Element einer Kreisschar mit einem Parameter
   	 
         *wert* : Wert des Scharparameters
   
   .. method:: schnitt(objekt)
   
         Schnittmenge des Kreises mit einem anderen Objekt; nur in der Ebene
		 
         *objekt* : Punkt, Gerade, Kreis
		 		 
         Zusatz: 
            `l=1` - Lageinformationen
			
            `exakt=nein` - näherungsweise Berechnung		 
   
   .. method:: tangente(punkt)
   
         Tangente in einem Kreispunkt oder von einem Punkt außerhalb; nur in der Ebene 
		 
         *punkt* : Kreispunkt oder Punkt außerhalb		 

   |
   
   **Synonyme Bezeichner**
   		
        ``fläche_  :  Fläche``
		
        ``gleich_  :  Gleich``
		
        ``in_kurve :  inKurve``
		
        ``is_schar :  isSchar``
		
        ``länge_   :  Länge``
				
        ``radius_  :  Radius``
		
        ``sch_el   :  schEl``
		
        ``sch_par  :  schPar``
		
        ``umfang_  :  Umfang``
   