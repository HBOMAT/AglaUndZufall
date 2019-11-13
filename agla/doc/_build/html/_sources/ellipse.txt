
Ellipse
=======

.. currentmodule:: agla.lib.objekte.ellipse

.. autoclass:: Ellipse
   
   **Eigenschaften und Methoden**
   
   */statt* ``ae`` *kann* ``ä`` *geschrieben werden/*   
   
   .. autoattribute:: hilfe
   
   .. autoattribute:: a
   
   .. autoattribute:: b
   
   .. autoattribute:: brenn_ger
   
         Synonym: **leit_ger**   
   
   .. autoattribute:: brenn_punkt
   
   .. autoattribute:: dim
         
   .. autoattribute:: flaeche
   
   .. method:: flaeche_()
   
         zugehörige Methode

         Zusatz :
		 
            `d=n` - Dezimalausgabe mit *n* Nachkomma-/Stellen 		 
		 
            `f=1` - Formel
   
   .. autoattribute:: F1

         Synonym: **f1**

   .. autoattribute:: F2

         Synonym: **f2**
   
   .. autoattribute:: gleich
   
   .. method:: gleich_(/[punkt])
   
         Auswertung der Gleichung in einem Punkt 

         Zusatz :  `g=ja` -  Bereitstellung der Gleichung als Gleichung-Objekt
		 
   .. autoattribute:: in_kurve
   
   .. autoattribute:: is_schar
      
   .. autoattribute:: lin_exz
   
         Synonym: **e**
		 
   .. autoattribute:: mitte
   
   .. autoattribute:: num_exz
   
         Synonym: **eps**
		 
   .. autoattribute:: prg
   
   .. autoattribute:: sch_par
   
   .. autoattribute:: umfang
   
   .. method:: bild(abbildung)
   
         Bildellipse bei einer Abbildung
		 
         *abbildung* : Abbildung
   
   .. method:: pkt(/[wert])
   
         Punkt der Ellipse

         *wert* : Wert des Ellipsenparameters (in Grad)		
		 
         Rückgabe : 						 
            bei Angabe eines Parameterwertes: 
               Ellipsenpunkt, der zu diesem Wert gehört
			   
            bei leerer Argumentliste oder freiem Bezeichner: 
               allgemeiner Punkt der Ellipse 
		 
   .. method:: sch_el(wert)
   
         Element einer Ellipsenschar mit einem Parameter
			
         *wert* : Wert des Scharparameters
		       
   .. method:: tangente(punkt)
   
         Tangente in einem Ellipsenpunkt

         *punkt* : Punkt der Ellipse		 
   
   |
   
   **Synonyme Bezeichner**
   
        ``hilfe       :  h``
		
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
   