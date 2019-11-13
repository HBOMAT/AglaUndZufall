
Dreieck
=======

.. currentmodule:: agla.lib.objekte.dreieck

.. autoclass:: Dreieck

   **Eigenschaften und Methoden**

   */statt* ``ae, oe`` *kann* ``ä, ö`` *geschrieben werden/*
   
   .. autoattribute:: hilfe
 	
   .. autoattribute:: A
   
   .. autoattribute:: B
   
   .. autoattribute:: C
   
   .. autoattribute:: a
   
   .. autoattribute:: b
   
   .. autoattribute:: c
   
   .. autoattribute:: alpha
   
   .. autoattribute:: beta
   
   .. autoattribute:: gamma
   
   .. autoattribute:: dim
   
   .. autoattribute:: ebene
   
   .. autoattribute:: flaeche
   
   .. method:: flaeche_()
   
         Flächeninhalt; Dezimaldarstellung
		 
         Zusatz : 
            `d=n` - mit *n* Nachkomma-/Stellen
			
            `f=1` - Formeln		 
   	    	 
   .. autoattribute:: in_figur
   
   .. autoattribute:: in_koerper
   
   .. autoattribute:: inkreis
   
   .. autoattribute:: is_recht_wink
   
   .. autoattribute:: is_schar
   
   .. autoattribute:: laengen
   
   .. method:: laengen_()
   
         Seitenlängen; Dezimaldarstellung
		 
         Zusatz : `d=n` - mit *n* Nachkomma-/Stellen   	    	 
   
   .. autoattribute:: punkte
   
   .. autoattribute:: sch_par
   
   .. autoattribute:: schwer_pkt
   
   .. autoattribute:: seiten
   
   .. method:: seiten_()

         zu seiten zugehörig; Erläuterung der Ausgabe
   
   .. autoattribute:: umfang
   
   .. method:: umfang_()
   
         Umfang; Dezimaldarstellung
		 
         Zusatz : `d=n` - mit *n* Nachkomma-/Stellen   	    	 
   
   .. autoattribute:: umkugel
   
   .. autoattribute:: winkel
   
   .. method:: winkel_()
   
         Innenwinkel; Dezimaldarstellung
		 
         Zusatz : `d=n` - mit *n* Nachkomma-/Stellen   	    	 
   
   .. autoattribute:: wink_summe

   .. method:: bild(abbildung)
   
         Bilddreieck bei einer Abbildung
		 
         *abbildung* : Abbildung
   
   .. method:: pkt(/[wert])   
   
         Punkt des Dreiecks  
   
         *wert* :
             Wert des Dreieckparameters (Parameter ist die Weglänge vom 
             ersten Punkt aus, die Gesamtlänge der Seiten wird auf 1 gesetzt
             - es ergeben sich Parameterwerte aus dem Intervall [0, 1])

         Rückgabe :   
            bei Angabe eines Parameterwertes:
               Dreieckpunkt, der zu diesem Wert gehört
            bei leerer Argumentliste oder freiem Bezeichner:
               allgemeiner Punkt des Dreiecks 			
   
   .. method:: sch_el(/[wert])
   
         Element einer Dreieckschar mit einem Parameter
   	 
         *wert* : Wert des Scharparameters
		          
   .. method:: schnitt(objekt)
   
         Schnittmenge des Dreiecks mit einem anderen Objekt
		 
         *objekt* im Raum : Punkt, Gerade
		 
         *objekt* in der Ebene : Punkt
		 		 
         Zusatz: `l=1` - Lageinformationen
   
|

   **Synonyme Bezeichner**
   
        ``hilfe         :  h``
		
        ``fläche_       :  Fläche``
		
        ``in_figur      :  inFigur``
		
        ``in_körper     :  inKörper``
		
        ``is_recht_wink :  isRechtWink``
		
        ``is_schar      :  isSchar``
		
        ``längen_       :  Längen``
		
        ``sch_el        :  schEl``
		
        ``sch_par       :  schPar``
		
        ``schwer_pkt    :  schwerPkt``
		
        ``seiten_       :  Seiten``
		
        ``umfang_       :  Umfang``
		
        ``winkel_       :  Winkel``
		
        ``wink_summe    :  winkSumme``
   
		   
   
   
   
   