
Viereck
=======

.. currentmodule:: agla.lib.objekte.viereck

.. autoclass:: Viereck

   **Eigenschaften und Methoden**

   */statt* ``ae`` *kann* ``ä`` *geschrieben werden/*
   
   .. autoattribute:: hilfe
   
         Synonym: **h**   
 	   
   .. autoattribute:: dim
   
   .. autoattribute:: dreiecke
   
   .. autoattribute:: ebene
   
   .. autoattribute:: flaeche
   
   .. method:: flaeche_()
   
         Flächeninhalt; Dezimaldarstellung
		 
         Zusatz : 
		 
            `d=n` - mit *n* Nachkomma-/Stellen
			
            `f=1` - Formeln		 
   	    	 
   .. autoattribute:: form
   
   .. autoattribute:: in_figur
   
   .. autoattribute:: in_koerper
   
   .. autoattribute:: is_konvex
   
   .. autoattribute:: is_pargramm
   
   .. autoattribute:: is_schar
   
   .. autoattribute:: laengen
   
   .. method:: laengen_()
   
         Seitenlängen; Dezimaldarstellung
		 
         Zusatz : `d=n` - mit *n* Nachkomma-/Stellen   	    	 
   
   .. autoattribute:: punkte
   
   .. method:: punkte_()
   
         zu punkte zugehörig; Erläuterung der Ausgabe   
   
   .. autoattribute:: sch_par
   
   .. autoattribute:: schwer_pkt
   
   .. autoattribute:: seiten
   
   .. method:: seiten_()

         zu seiten zugehörig; Erläuterung der Ausgabe
		 
   .. autoattribute:: umfang		 
   
   .. method:: umfang_()
   
         Umfang; Dezimaldarstellung
		 
         Zusatz : `d=n` - mit *n* Nachkomma-/Stellen  	    	 
      
   .. autoattribute:: winkel
   
   .. method:: winkel_()
   
         Innenwinkel; Dezimaldarstellung
		 
         Zusatz : `d=n` - mit *n* Nachkomma-/Stellen   	    	 
   
   .. method:: bild(abbildung)
   
         Bildviereck bei einer Abbildung
		 
         *abbildung* : Abbildung
   
   .. method:: pkt(/[wert])   
   
         Punkt des Vierecks  
   
         *wert* :
             Wert des Viereckparameters (Parameter ist die Weglänge vom 
             ersten Punkt aus, die Gesamtlänge der Seiten wird auf 1 gesetzt - 
             es ergeben sich Parameterwerte aus dem Intervall [0, 1])

         Rückgabe :   
            bei Angabe eines Parameterwertes:
               Viereckpunkt, der zu diesem Wert gehört
            bei leerer Argumentliste oder freiem Bezeichner:
               allgemeiner Punkt des Vierecks 			
   
   .. method:: sch_el(/[wert])
   
         Element einer Viereckschar mit einem Parameter
   	 
         *wert* : Wert des Scharparameters
		          
   .. method:: schnitt(objekt)
   
         Schnittmenge des Vierecks mit einem anderen Objekt
		 
         *objekt* im Raum : Punkt, Gerade
		 
         *objekt* in der Ebene : Punkt
		 		 
         Zusatz: `l=1` - Lageinformationen
   
|

   **Synonyme Bezeichner**
   		
        ``fläche_       :  Fläche``
		
        ``in_figur      :  inFigur``
		
        ``in_körper     :  inKörper``
		
        ``is_pargramm   :  isPargramm``
		
        ``is_schar      :  isSchar``
		
        ``längen_       :  Längen``
		
        ``punkte_       :  Punkte``
		
        ``sch_el        :  schEl``
		
        ``sch_par       :  schPar``
		
        ``schwer_pkt    :  schwerPkt``
		
        ``seiten_       :  Seiten``
		
        ``umfang_       :  Umfang``
		
        ``winkel_       :  Winkel``
		   
		   
   
   
   
   