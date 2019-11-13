
MK - MarkoffKette
=================

.. currentmodule:: zufall.lib.objekte.markoff_kette

.. autoclass:: MarkoffKette

   **Eigenschaften und Methoden**
   
   */statt* ``ae`` *kann* ``ä`` *geschrieben werden/*
   
   .. autoattribute:: hilfe
   
         Synonym: **h**   
      
   .. autoattribute:: bez              
   
   .. autoattribute:: diagr
   
   .. autoattribute:: dim
   
   .. autoattribute:: fix_vekt
   
         Synonym: **stat_vert**
		 
   .. autoattribute:: grenz
   
   .. autoattribute:: is_regulaer
   
   .. autoattribute:: matrix   
   
   .. method:: matrix(_)  

         Übergangsmatrix; zugehörige Methode

         Zusatz:  `b=ja` -  Ausgabe mit Bezeichnern		 
   
   .. autoattribute:: start
   
   .. method:: zustand(n)   

         Zustandsvektor nach *n* Schritten
		 
         *n* : Anzahl Schritte, *n* >= 0   
   
   |

   **Synonyme Bezeichner**

      ``fix_vekt    :  fixVekt``
	  
      ``is_regulär  :  isRegulär``
	  
      ``matrix_     :  Matrix``
	  
      ``stat_vert   : statVert``

      
