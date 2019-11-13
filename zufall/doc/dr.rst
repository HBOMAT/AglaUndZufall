
DR - DatenReihe
===============


.. currentmodule:: zufall.lib.objekte.datenreihe

.. autoclass:: DatenReihe
   
   **Eigenschaften und Methoden**
   
   .. autoattribute:: hilfe
   
         Synonym: **h**   
      
   .. autoattribute:: box_plot
      
   .. method:: box_plot_()
   
        Boxplot-Diagramm; zugehörige Methode 

        Zusatz: `e=ja` - Erläuterungen zum Diagramm		
      
   .. autoattribute:: daten
      
   .. autoattribute:: diagr
   
   .. autoattribute:: graf_F
   
   .. method:: F(wert)
   
         Empirische Verteilungsfunktion
		 
         *wert* : Zahl

         Zusatz:
            `d=n`    Darstellung dezimal mit *n* Kommastellen

            `b=ja`   Erläuterung des Begriffes			
    
   .. method:: hh(ereignis)
   
         Relative Häufigkeiten
		 
         *ereignis* :    *elem* | *Liste/Tupel/Menge* von elem's
		 
         *elem* :        Element der Datenliste
		 
         Zusatz:
            `p=ja` -     Ausgabe als Prozentwert
			
            `d=n` -      Ausgabe dezimal mit *n* Kommastellen
			
            `ah=ja` -    Ausgabe aller Häufigkeiten der Datenelemente
 
            `ap=ja` -    ebenso, Prozentwerte

            `ad=n` -     ebenso, Dezimalzahlen mit *n* Kommastellen 
   
            `ahd=ja` -   Rückgabe als dictionary

            `adp=ja` -   ebenso, Prozentwerte

            `add=n` -    ebenso, Dezimalzahlen
		 	 
   .. method:: H(ereignis)
   
         Absolute Häufigkeiten   
   
         *ereignis* :    *elem* | *Liste/Tupel/Menge* von elem's
		 
         *elem* :        Element der Datenliste
		 
         Zusatz:
            `d=ja` -     Ausgabe aller Häufigkeiten als dictionary   
   
            `s=ja` -     ebenso, Spaltenausgabe   
   
   .. autoattribute:: halb_weite
   
   .. method:: halb_weite_()
   
         Halbweite; zugehörige Methode

         Zusatz: `e=ja` - Erläuterung		 
      
   .. autoattribute:: hist
   
         Synonym: **hist_rel_h**   
   
   .. method:: hist_()
   
         Histogramm; zugehörige Methode

         Zusatz: 
            `p=ja` - Polygonzug	

            Angabe einer ZufallsGröße | DatenReihe - Vergleich mit anderer 
            Verteilung
			
   .. autoattribute:: hist_abs_h 
   
   .. autoattribute:: hist_kum
      	
   .. autoattribute:: is_ganz
	
   .. method:: klassen(anzahl )
   
         KLasseneinteilung

         *anzahl* : Anzahl Klassen		 
   
         Die Klassen haben gleiche Breite und folgen unmittelbar aufeinander

         Die zurückgegebene DatenReihe beinhaltet für alle Datenelemente den 
         Index der Klasse, in der das Datenelement liegt		 
   
         Zusatz: `g=la` - Ausgabe der Klassengrenzen		 
   
   .. method:: korr_koeff(dr)
   
         Korrelationskoeffizient für zwei DatenReihen

         *dr* : DatenReihe
		    
   .. autoattribute:: linien
   
   .. autoattribute:: max
   
   .. autoattribute:: min
   
   .. autoattribute:: mittel
   
   .. method:: mittel_()
       
         Arithmetischer Mittelwert; zugehörige Methode   
   
         Zusatz:			
            `d=n` - Darstellung dezimal mit *n* Kommastellen
			
            `f=ja` - Berechnungsformel					 
   
   .. autoattribute:: modal
   
   .. method:: modal_()
   
         Modalwert(e); zugehörige Methode

         Zusatz:			
            `r=ja` - relative Häufigkeit

            `rd=ja` - ebenso, dezimal
			
            `e=ja` - Erläuterung
			       
   .. autoattribute:: o_quartil
   
   .. method:: o_quartil_()

         Oberes Quartil; zugehörige Methode
   
         Zusatz: `b=ja` - Berechnung
   
   .. autoattribute:: poly_zug
   
   .. method:: quantil(q)
   
         Quantile   
   
         *q* : Zahl aus [0, 1]   
   
   .. autoattribute:: s
 
   .. method:: s_()
  
         Standardabweichung; zugehörige Methode   
  
         Zusatz: 
            `d=ja` - Darstellung dezimal mit *n* Kommastellen		 
		
            `b=ja` - Berechnung		 		
		
   .. autoattribute:: spann_weite
   
   .. method:: spann_weite_()
  
         Spannweite; zugehörige Methode   
  
         Zusatz: `b=ja` - Berechnung		 
   
   .. method:: streu_diagr(dr)
  
         Streudiagramm mit Regressionsgerade für zwei Datenreihen

         *dr* : DatenReihe
		 
         Zusatz: `g=ja` - Gleichung der Regressionsgeraden		       		 
  
   .. autoattribute:: umfang
   
         Sybonym: **n**   
   
   .. autoattribute:: u_quartil
   
   .. method:: u_quartil_()
   
         Unteres Quartil; zugehörige Methode
   
         Zusatz: `b=ja` - Berechnung
   
   .. autoattribute:: var
   
   .. method:: var_()
   
         Varianz; zugehörige Methode
		 
         Zusatz: 
            `d=n` - Darstellung dezimal mit *n* Kommastellen
			
            `a=ja` - Berechnung mit 1/(*n*-1)
			
            `ad=ja` - ebenso, Darstellung dezimal
			
            `f=ja` - Berechnungsformeln
			   
   .. autoattribute:: vert
   
         Synonym: **vert_rel_h**   
   
   .. method:: vert_()
   
         Verteilung der relativen Häufigkeiten; zugehörige Methode  
   
         Synonym: **vert_rel_h_**

         Zusatz: 
            `p=ja` relative Häufigkeiten werden als Prozentwerte ausgegeben	

            `d=n` ebenso, dezimal mit *n* Kommastellen		
		 
            `s=ja` Spaltenausgabe	

            `sp=ja` ebenso, Prozentwerte	

            `sd=n` ebenso, dezimal mit *n* Kommastellen		
		 
   .. autoattribute:: vert_abs_h
   
   .. method:: vert_abs_h_()
   
         Verteilung der absoluten Häufigkeiten; zugehörige Methode 

         Zusatz: `s=ja` Spaltenausgabe	
  		 
   .. autoattribute:: vert_kum

   .. method:: vert_kum_()
  
         Kumulierte Häufigkeitskeitsverteilung; zugehörige Methode 

         Zusatz: 
            `p=ja` relative Häufigkeiten werden als Prozentwerte ausgegeben	

            `d=n` ebenso, dezimal mit *n* Kommastellen		
		 
            `s=ja` Spaltenausgabe	

            `sp=ja` ebenso, Prozentwerte	

            `sd=n` ebenso, dezimal mit *n* Kommastellen		

   .. autoattribute:: violin_plot
   
   .. method:: violin_plot_h_()

        Violinplot-Diagramm; zugehörige Methode   

        Zusatz: `e=ja` - Erläuterungen zum Diagramm		
		
|

   **Synonyme Bezeichner**
   		   	
     ``box_plot     :  boxPlot``
		
     ``box_plot_    :  BoxPlot``
	 
     ``graf_F       :  grafF``
	 
     ``halb_weite   :  halbWeite``
	 
     ``halb_weite_  :  HalbWeite``
	 
     ``hist_        :  Hist``
	 
     ``hist_abs_h   :  histAbsH``
	 
     ``hist_kum     :  histKum``
	 
     ``hist_rel_h   :  histRelH``
	 
     ``is_ganz      :  isGanz``
	 
     ``korr_koeff   :  korrKoeff``
	 
     ``mittel_      :  Mittel``
	 
     ``o_quartil    :  oQuartil``
	 
     ``o_quartil_   :  OQuartil``
	 
     ``poly_zug     :  polyZug``
	 
     ``poly_zug_    :  PolyZug``
	 
     ``modal_       :  Modal``
	 
     ``s_           :  S``
	 
     ``spann_weite  :  spannWeite``
	 
     ``spann_weite_ :  SpannWeite``
	 
     ``streu_diagr  :  streuDiagr``
	 
     ``u_quartil    :  uQuartil``
	 
     ``u_quartil_   :  UQuartil``
	 
     ``var_         :  Var``
	 
     ``vert_        :  Vert``
	 
     ``vert_abs_h   :  vertAbsH``
	 
     ``vert_abs_h_  :  VertAbsH``
	 
     ``vert_kum     :  vertKum``
	 
     ``vert_kum_    :  VertKum``
	 
     ``vert_rel_h   :  vertRelH``
	 
     ``vert_rel_h_  :  VertRelH``
	 
     ``violin_plot  :  violinPlot``
	 
     ``violin_plot_ :  ViolinPlot``
