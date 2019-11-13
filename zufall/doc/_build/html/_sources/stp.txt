
STP - SignifikanzTestP
======================

.. currentmodule:: zufall.lib.objekte.signifikanz_test_p   

.. autoclass:: SignifikanzTestP
   
   **Eigenschaften und Methoden**
   
   */statt* ``ue`` *kann* ``ü`` *geschrieben werden/*

   .. autoattribute:: hilfe
   
         Synonym: **h**   
      
   .. autoattribute:: ab_ber
   
   .. method:: ab_ber_()
   
        Ablehnungsbereich von :math:`H_0`; zugehörige Methode  

        Zusatz: `g=ja` Grafische Darstellung	
   
   .. autoattribute:: an_ber
   
   .. method:: an_ber_()
   
        Annahmebereich von :math:`H_0`; zugehörige Methode  

        Zusatz: `g=ja` Grafische Darstellung	   
   
   .. autoattribute:: alpha
 
   .. autoattribute:: begriffe
    
   .. autoattribute:: bv
   
   .. method:: guete(p)
   
         Güte-Funktion
		 
         *p* : Zahl aus [0, 1]		 

         Zusatz: `g=ja`   Graf der Funktion		 
   
   .. autoattribute:: h0
   
         Synonym: **H0**
         
   .. autoattribute:: h1
  
         Synonym: **H1**
  
   .. autoattribute:: k
   
         Synonym: **K**
   
   .. autoattribute:: n
   
   .. method:: oc(p)
   
         Operationscharakteristik-Funktion

         Synonym: **beta**	

         *p* : Zahl aus [0, 1]		 

         Zusatz: `g=ja`   Graf der Funktion		 		 
   
   .. method:: quantil_bv(q)
   
         Quantile der Binomialverteilung bei :math:`H_0`
   
         *q* : Zahl aus [0, 1]		 
   
   .. method:: quantil_nv(q)
   
         Quantile der (0,1)-Normalverteilung
		 
         *q* : Zahl aus [0, 1]		 

   .. autoattribute:: regel
   
   .. method:: regel_()
   
         Entscheidungsregel; zugehörige Methode   
   
         Zusatz:   `g=ja`   Grafische Darstellung   
		 
   .. autoattribute:: schema
   
   .. autoattribute:: sig_niv	 
		 
|

   **Synonyme Bezeichner**
   		
        ``ab_ber      :  abBer``
	
        ``an_ber      :  anBer``
		
        d``beta_       :  Beta``

        ``quantil_bv  :  quantilBV``
		
        ``quantil_nv  :  quantilNV``
   
        ``regel_      :  Regel``
	
        ``sig_niv     :  sigNiv``
	
	
