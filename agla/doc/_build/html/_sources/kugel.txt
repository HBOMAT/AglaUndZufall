
Kugel
=====

.. currentmodule:: agla.lib.objekte.kugel

.. autoclass:: Kugel


   **Eigenschaften und Methoden**

   */statt* ``ae`` *kann* ``ä`` *geschrieben werden/*
   
   .. autoattribute:: hilfe
   
         Synonym: **h**
		 
   .. autoattribute:: dim
   
   .. autoattribute:: flaeche
   
   .. method:: flaeche_()

         Oberflächeninhalt ; Dezimaldarstellung
		 
         Zusatz : *d=n* - mit *n* Nachkomma-/Stellen   
   
   .. autoattribute:: gleich
   
   .. method:: gleich_(punkt | [x, y] | (x, y))
   
         Auswertung der Gleichung in einem Punkt 

         *punkt* : Punkt		 
   
         Bei Angabe von *x*, *y* Rückgabe der/des zum entsprechenden Punkt
         der *xy* - Ebene gehörenden Kugelpunkte/-s   
   
   .. autoattribute:: in_flaeche
   
   .. autoattribute:: is_schar
   
   .. autoattribute:: mitte
   
         Synonyme: **M**, **m**    
   
   .. autoattribute:: o_flaeche 
   
   .. method:: o_flaeche_()
   
         Oberflächeninhalt; Dezimaldarstellung
		 
         Zusatz : *d=n* - mit *n* Nachkomma-/Stellen      
   
   .. autoattribute:: radius

         Synonym: **r**    
   
   .. method:: radius_()

         Synonym: **r_**    
   
         Radius; Dezimaldarstellung
		 
         Zusatz : *d=n* - mit *n* Nachkomma-/Stellen      
   
   .. autoattribute:: sch_par
   
   .. autoattribute:: volumen
   
   .. method:: volumen_()
   
         Volumen; Dezimaldarstellung
		 
         Zusatz : *d=n* - mit *n* Nachkomma-/Stellen      
    
   .. method:: abstand(objekt)   
   
         Abstand der Kugel zu einem anderen Objekt
      
         *objekt* : Punkt, Gerade, Ebene, Kugel
		 
         Zusatz : *d=n* - mit *n* Nachkomma-/Stellen
			
         Rückgabe :  0, wenn die Kugel *objekt* schneidet	
   
   .. method:: bild(abbildung)
   
         Bildkugel bei einer Abbildung
		 
         *abbildung* : Abbildung des Raumes
   
   
   .. method:: sch_el(wert)
   
         Element einer Kugelschar mit einem Parameter
			
         *wert* : Wert des Scharparameters
   
   .. method:: schnitt(objekt)
   
         Schnittmenge der Kugel mit einem anderen Objekt
		 
         *objekt* : Punkt, Gerade, Ebene, Kugel
		 		 
         Zusatz: *l=1* - Lageinformationen
   
   
   .. method:: tangenten(punkt)
		
         Tangenten an die Kugel	von einem Punkt außerhalb oder von einem
         Punkt der Kugeloberfläche

         *punkt* : Punkt

         Rückgabe :   
            bei einem Punkt außerhalb:
               Berührkreis; seine Trägerebene ist die Polarebene
               :func:`kugel.tangenten(punkt).ebene`
            bei einem Kugelpunkt:
               Tangentialebene
				
|
   
   **Synonyme Bezeichner**
	  
      ``fläche_     :  Fläche``
	  
      ``gleich_     :  Gleich``
	  
      ``in_fläche   :  inFläche``
	  
      ``is_schar    :  isSchar``
	  
      ``o_fläche    :  oFläche``
	  
      ``radius_     :  Radius``
	  
      ``sch_el      :  schEl``
	  
      ``sch_par     :  schPar``
	  
      ``volumen_    :  Volumen``
		
		
