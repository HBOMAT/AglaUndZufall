
Zylinder
========

.. currentmodule:: agla.lib.objekte.zylinder

.. autoclass:: Zylinder
   
   **Eigenschaften und Methoden**

   */statt* ``ae, oe`` *kann* ``ä, ö`` *geschrieben werden/*
      
   .. autoattribute:: hilfe
   
         Synonym: **h**   
   
   .. autoattribute:: deck
      
   .. autoattribute:: dim
   
   .. autoattribute:: g_flaeche
   
   .. method:: g_flaeche_()

         Grundflächeninhalt; Dezimaldarstellung  
		 
         Zusatz : 
            `d=n` - mit *n* Nachkomma-/Stellen 		 		 
		 
            `f=1` - Formel			
		 
   .. autoattribute:: grund
   
   .. autoattribute:: hoehe

   .. method:: hoehe_()

         Höhe; Dezimaldarstellung  
		 
         Zusatz : `d=n` - mit *n* Nachkomma-/Stellen 		 
		    
   .. autoattribute:: is_schar
   
   .. autoattribute:: m_flaeche
   
   .. method:: m_flaeche_()
   
         Mantelflächeninhalt; Dezimaldarstellung  
		 
         Zusatz : 
            `d=n` - mit *n* Nachkomma-/Stellen 		  		 
		    
            `f=1` - Formel			
			
   .. autoattribute:: o_flaeche

   .. method:: o_flaeche_()
   
         Oberflächeninhalt; Dezimaldarstellung  
		 
         Zusatz : 
            `d=n` - mit *n* Nachkomma-/Stellen 		  		 
		    
            `f=1` - Formel			
			
   .. autoattribute:: sch_par
      
   .. autoattribute:: volumen
   
   .. method:: volumen_()
   
         Volumen; Dezimaldarstellung  
		 
         Zusatz : 
            `d=n` - mit *n* Nachkomma-/Stellen 		 

            `f=1` - Formel			
		    
   .. method:: bild(abbildung)
   
         Bildzylinder bei einer Abbildung
		 
         *abbildung* : Abbildung des Raumes 
   
   .. method:: sch_el(wert)

         Element einer Zylinderschar mit einem Parameter
   	 
         *wert* : Wert des Scharparameters
   
   |
			
   **Synonyme Bezeichner**
   		
        ``g_fläche  :  gFläche``
		
        ``g_fläche_ :  GFläche``
		
        ``höhe_     :  Höhe``
		
        ``is_schar  :  isSchar``
		
        ``m_fläche  :  mFläche``
		
        ``m_fläche_ :  MFläche``
		
        ``o_fläche  :  oFläche``
		
        ``o_fläche_ :  OFläche``
		
        ``sch_el    :  schEl``
		
        ``sch_par   :  schPar``
		
        ``volumen_  :  Volumen``
			
			
			