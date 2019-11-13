
VT - VierFelderTafel
====================

.. currentmodule:: zufall.lib.objekte.vier_felder_tafel

.. autoclass:: VierFelderTafel

   **Eigenschaften und Methoden**
   
   .. autoattribute:: hilfe
   
         Synonym: **h**   
      
   .. autoattribute:: abs_h
      
         Synonym: **nat_h**
	  
   .. method:: abs_h_( /[grund] )
   
         Tafel mit absoluten Häufigkeiten; zugehörige Methode   

         *grund*:   Grundwert
            alle Tafelwerte werden auf diesen Wert umgerechnet; falls nicht 
            angegeben, ist der Grundwert die (eventuell gerundete) 
            Zeilen-/Spaltensumme der Tafelwerte
			
   .. autoattribute:: ausg
   
   .. autoattribute:: baum
   
   .. method:: baum_()
   
         Baumdiagramm; zugehörige Methode

         Zusatz:
            `p=ja` - Wahrscheinlichkeiten werden als Prozentwerte ausgegeben
			
            `d=n`  - Wahrscheinlichkeiten werden als Dezimalzahlen mit *n* 
            Kommastellen ausgegeben
		 
   .. autoattribute:: chi2_test
   
   .. autoattribute:: fisher_test
   
   .. autoattribute:: hb
   
   .. method:: hb_( /[grund] )
      
         Häufigkeitsbaum; zugehörige Methode
		     
         *grund*:   Grundwert
            alle Tafelwerte werden auf diesen Wert umgerechnet; falls nicht 
            angegeben, ist der Grundwert die (eventuell gerundete) 
            Zeilen-/Spaltensumme der Tafelwerte			 
			 
   .. autoattribute:: umkehr
   
   .. autoattribute:: wahrsch
   
   **Synonyme Bezeichner**

      ``abs_h       :  absH``

      ``abs_h_      :  AbsH``

      ``baum_       :  Baum``

      ``chi2_test   :  chi2Test``

      ``fisher_test : fisherTest``

      ``hb_         :   Hb``

      ``nat_h       :   natH``

      ``nat_h_      :  NatH``

      ``rel_h       :  relH``
