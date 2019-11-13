
Pyramide
========

.. currentmodule:: agla.lib.objekte.pyramide

.. autoclass:: Pyramide
   
   **Eigenschaften und Methoden**

   */statt* ``ae``, ``oe`` *kann* ``ä``, ``ö`` *geschrieben werden/*
   
   .. autoattribute:: hilfe
   
         Synonym: **h**   
   
   .. autoattribute:: dim
   
   .. autoattribute:: g_flaeche
   
   .. method:: g_fläche_()

         Grundflächeninhalt; Dezimaldarstellung  
		 
         Zusatz : `d=n` - mit *n* Nachkomma-/Stellen		 
		 
   .. autoattribute:: grund
   
   .. autoattribute:: hoehe

   .. method:: hoehe_()

         Höhe; Dezimaldarstellung  
		 
         Zusatz : `d=n` - mit *n* Nachkomma-/Stellen 		 
		 
   .. autoattribute:: in_koerper
   
   .. autoattribute:: is_schar
   
   .. autoattribute:: m_flaeche
   
   .. method:: m_flaeche_()
   
         Mantelflächeninhalt; Dezimaldarstellung  
		 
         Zusatz : `d=n` - mit *n* Nachkomma-/Stellen 		 
		    
   .. autoattribute:: o_flaeche

   .. method:: o_flaeche_()
   
         Oberflächeninhalt; Dezimaldarstellung  
		 
         Zusatz : `d=n` - mit *n* Nachkomma-/Stellen	 
		    
   .. autoattribute:: sch_par
   
   .. autoattribute:: seiten
   
   .. autoattribute:: spitze
   
   .. autoattribute:: volumen
   
   .. method:: volumen_()
   
         Volumen; Dezimaldarstellung  
		 
         Zusatz : 
            `d=n` - mit *n* Nachkomma-/Stellen
			
            `f=1` - Formel			

   .. method:: bild(abbildung)
   
         Bildpyramide bei einer Abbildung
		 
         *abbildung* : Abbildung des Raumes 
   
   .. method:: sch_el(wert)

         Element einer Pyramidenschar mit einem Parameter
   	 
         *wert* : Wert des Scharparameters
   
   |

   **Synonyme Bezeichner**
   		
        ``g_fläche  :  gFläche``
		
        ``g_fläche_ :  GFläche``
		
        ``höhe_     :  Höhe``
		
        ``in_körper :  inKörper``
		
        ``is_schar  :  isSchar``
		
        ``m_fläche  :  mFläche``
		
        ``m_fläche_ :  MFläche``
		
        ``o_fläche  :  oFläche``
		
        ``o_fläche_ :  OFläche``
		
        ``sch_el    :  schEl``
		
        ``sch_par   :  schPar``
		
        ``volumen_  :  Volumen``
   
   
   