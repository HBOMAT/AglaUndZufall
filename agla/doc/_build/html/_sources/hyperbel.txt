
Hyperbel
========

.. currentmodule:: agla.lib.objekte.hyperbel

.. autoclass:: Hyperbel
   
   **Eigenschaften und Methoden**
      
   .. autoattribute:: hilfe
   
         Synonym: **h**   
   
   .. autoattribute:: a
   
   .. autoattribute:: b

   .. autoattribute:: asympt
   
   .. autoattribute:: brenn_punkt
   
   .. autoattribute:: dim
   
   .. autoattribute:: F1
   
         Synonym: **f1**   
   
   .. autoattribute:: F2
   
         Synonym: **f2**   
      
   .. autoattribute:: gleich
   
   .. method:: gleich_(/[punkt])
   
         Auswertung der Gleichung in einem Punkt 

         Zusatz :  `g=ja` - Bereitstellung der Gleichung als Gleichung-Objekt
		 
   .. autoattribute:: in_kurve
   
   .. autoattribute:: is_schar
      
   .. autoattribute:: leit_ger
   
         Synonym: **brenn_ger**   
   	  
   .. autoattribute:: lin_exz
   
         Synonym: **e**   
		 
   .. autoattribute:: mitte
   
   .. autoattribute:: num_exz
   
         Synonym: **eps**   
		 
   .. autoattribute:: prg
   
   .. autoattribute:: prg_hf
   
   .. autoattribute:: prg_rf
   
   .. autoattribute:: sch_par
      
   .. method:: bild(abbildung)
   
         Bildhyperbel bei einer Abbildung
		 
         *abbildung* : Abbildung
   
   .. method:: pkt(/[wert] )
   
         Punkt der Hyperbel

         *wert* : Wert des Hyperbelparameters (in Radian)		
		 
         Rückgabe : 						 
            bei Angabe eines Parameterwertes: 
               Hyperbelpunkt, der zu diesem Wert gehört
			   
            bei leerer Argumentliste oder freiem Bezeichner: 
               allgemeiner Punkt der Hyperbel 
		 
   .. method:: sch_el(wert )
   
         Element einer Hyperbelschar mit einem Parameter
			
         *wert* : Wert des Scharparameters
		       
   .. method:: tangente(punkt )
   
         Tangente in einem Hyperbelpunkt

         *punkt* : Punkt der Hyperbel		 
   
   |
   
   **Synonyme Bezeichner**
   		
        ``brenn_ger   :  brennGer``
		
        ``brenn_punkt :  brennPunkt``
		
        ``fläche_     :  Fläche``
		
        ``gleich_     :  Gleich``
		
        ``in_kurve    :  inKurve``
		
        ``is_schar    :  isSchar``
				
        ``leit_ger    :  leitGer``
		
        ``lin_exz     :  linExz``
		
        ``num_exz     :  numExz``
		
        ``sch_el      :  schEl``
		
        ``sch_par     :  schPar``
      