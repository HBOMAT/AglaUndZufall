
Parabel
=======

.. currentmodule:: agla.lib.objekte.parabel

.. autoclass:: Parabel
   
   **Eigenschaften und Methoden**
      
   .. autoattribute:: hilfe 
   
         Synonym: **h**

   .. autoattribute:: brenn_ger
   
         Synonym: **leit_ger**
   
   .. autoattribute:: brenn_punkt
   
         Synonyme: **F**, **f**
   
   .. autoattribute:: dim
   
   .. autoattribute:: gleich
   
   .. method:: gleich_(/[punkt])
   
         Auswertung der Gleichung in einem Punkt 
		 
         *punkt* : Punkt		 

         Zusatz :  `g=ja` - Bereitstellung der Gleichung als Gleichung-Objekt
		 
   .. autoattribute:: in_kurve
   
   .. autoattribute:: is_schar
      
   .. attribute:: lin_exz
   
         Synonym: **e**
   		
   .. attribute:: num_exz
   
         Synonym: **eps**
   
   .. autoattribute:: p

   .. autoattribute:: prg
   
   .. autoattribute:: scheitel
      
   .. autoattribute:: sch_par
      
   .. method:: bild(abbildung)
   
         Bildparabel bei einer Abbildung
		 
         *abbildung* : Abbildung
   
   .. method:: pkt(/[wert] )
   
         Punkt der Parabel

         *wert* : Wert des Parabelparameters	
		 
         Rückgabe : 						 
            bei Angabe eines Parameterwertes: 
               Parabelpunkt, der zu diesem Wert gehört			  
            bei leerer Argumentliste oder freiem Bezeichner: 
               allgemeiner Punkt der Parabel 
		 
   .. method:: sch_el(wert)
   
         Element einer Parabelschar mit einem Parameter
			
         *wert* : Wert des Scharparameters
		       
   .. method:: tangente(punkt)
   
         Tangente in einem Parabelpunkt

         *punkt* : Punkt der Parabel		 
   
   |
   
   **Synonyme Bezeichner**
   
        ``brenn_ger   :  brennGer``
		
        ``brenn_punkt :  brennPunkt``
				
        ``gleich_     :  Gleich``
		
        ``in_kurve    :  inKurve``
		
        ``is_schar    :  isSchar``
				
        ``leit_ger    :  leitGer``
		
        ``lin_exz     :  linExz``
		
        ``num_exz     :  numExz``
		
        ``sch_el      :  schEl``
		
        ``sch_par     :  schPar``
         