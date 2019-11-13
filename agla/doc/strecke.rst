
Strecke
=======

.. currentmodule:: agla.lib.objekte.strecke

.. autoclass:: Strecke
   
   **Eigenschaften und Methoden**

   */statt* ``ae`` *kann* ``ä`` *geschrieben werden/*
   
   .. autoattribute:: hilfe
   
         Synonym: **h**   

   .. autoattribute:: anf

   .. autoattribute:: dim
   
   .. autoattribute:: end
   
   .. autoattribute:: gerade
    
   .. autoattribute:: in_figur
   
   .. autoattribute:: in_koerper
         
   .. autoattribute:: is_schar
   
   .. autoattribute:: laenge
   
   .. method:: laenge_()   

         Länge; Dezimaldarstellung
		 
         Zusatz : `d=n` - mit *n* Nachkomma-/Stellen      
   
   .. autoattribute:: mitte
   
   .. autoattribute:: punkte
   
   .. autoattribute:: sch_par
   
   .. method:: bild(abbildung)
   
         Bildstrecke bei einer Abbildung
		 
         *abbildung* : Abbildung
   
   .. method:: pkt(/[wert])   
   
         Punkt der Strecke   
   
         *wert* : Wert des Streckenparameters aus [0, 1]

         Rückgabe :   
            bei Angabe eines Parameterwertes:
               Streckenpunkt, der zu diesem Wert gehört
					  
            bei leerer Argumentliste oder freiem Bezeichner:
               allgemeiner Punkt der Strecke 			
   
   .. method:: sch_el(wert)  
   
         Element einer Streckenschar mit einem Parameter
			
         *wert* : Wert des Scharparameters   
   
   .. method:: schnitt(objekt) 

         Schnittmenge der Strecke mit einem anderen Objekt
		 
         *objekt* im Raum : Punkt, Gerade, Ebene, Strecke
		 
         *objekt* in der Ebene : Punkt, Gerade, Strecke
		 		 				 
         Zusatz: `l=1` - Lageinformationen
      
   .. method:: teil_punkt(k)
   
         Teilpunkt 

         *k* : Teilverhältnis		 

   .. method:: teil_verh(punkt)
   
         Teilverhältnis

         *punkt* : Punkt der Trägergeraden		 

   |
   
   **Synonyme Bezeichner**
   	  
      ``in_figur   :  inFigur``
	  
      ``in_körper  :  inKörper``
	  
      ``is_schar   :  isSchar``
	  
      ``länge_     :  Länge``

      ``sch_el     :  schEl``

      ``sch_par    :  schPar``
	  
      ``teil_punkt :  teilPunkt``
	  
      ``teil_verh  :  teilVerh``
	  
	  
   