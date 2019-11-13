
Funktionen 
==========

Als *zahl* ist auch jeder Ausdruck zu verstehen, dessen Evaluierung (nach 
einer eventuellen Substitution von Variablen durch Zahlen) eine Zahl ergibt

Allgemeine Funktionen
---------------------

*/statt* ``oe``, ``ae`` *kann* ``ö``, ``ä`` *geschrieben werden/*

   .. function:: Hilfe()
   
         Hilfefunktion 

         Zusatz: `h=n`, *n = 1, 2, ...*		 

   .. function:: fakultaet( n ) 
   
         Fakultäts - Funktion
		 
         Synonym:   **fak**
   
         *n* : ganze Zahl >= 0
		  
   .. function:: binomial( n, k )
   
         Binomialkoeffizient
		 
         Synonym:   **B** *kann überschrieben werden!*
   
         *n*, *k* : ganze Zahl >= 0
		 
   .. function:: permutationen( menge | n )
   
         Permutationen einer Menge von Elementen
		 
         Synonym:   **perm**   

         *menge* : 
		 
            | *Liste/Tupel/Menge* von Elementen | *dictionary* 
            | Elemente sind Zahlen, Symbole, Zeichenketten
            | ein dictionary enthält (*element:anzahl*)-Paare
			
         *n* : ganze Zahl > 0; es  wird die Menge {*1, 2,...,n*} verwendet
		 
         Zusatz:
            `k=ja` -  Ausgabe der Permutationen in Kurzform
			
            `l=ja` - Ausgabe der Permutationen in Listenform
			
            `f=ja` - Formeln
 
   .. function:: kombinationen( menge, k, wiederh, anordn )
   
         *k*-Kombinationen aus einer Menge von Elementen    

         Synonym:   **komb**   
		 
         *menge* :
		 
            | *Liste/Tupel/Menge* von Elementen | *dictionary* | 
            | ganze Zahl *n* > 0
            | Elemente sind Zahlen, Symbole, Zeichenketten
            | ein dictionary enthält (*element:anzahl*)-Paare
            | bei Angabe von *n* wird die Menge 
            | {*1, 2,...,n*} verwendet
			
         *k* : ganze Zahl > 0; Anzahl der Elemente einer Kombination
		 
         *wiederh* :  Wiederholungen von Elementen in einer Kombination 
         möglich (``ja/nein``)
		 
         *anordn* :   Beachtung der Anordnung / Reihenfolge der 
         Elemente in einer Kombination (``ja/nein``)
		 
         Zusatz:
            `k=ja` -  Ausgabe der Kombinationen in Kurzform
			
            `l=ja` - Ausgabe der Kombinationen in Listenform
					 
            `f=ja` -  Formeln
			
            `b=ja` - Begriffe
		 
   .. function:: variationen( menge, k, wiederh )
   
         Variationen aus einer Menge von Elementen    
		 
         *menge* :
		 
            | *Liste/Tupel/Menge* von Elementen | *dictionary* | 
            | ganze Zahl *n* > 0
            | Elemente sind Zahlen, Symbole, Zeichenketten
            | ein dictionary enthält (*element:anzahl*)-Paare
            | bei Angabe von *n* wird die Menge 
            | {*1, 2,...,n*} verwendet
			
         *k* : ganze Zahl > 0; Anzahl der Elemente einer Variation
		 
         *wiederh* :  Wiederholungen von Elementen in einer Variation 
         möglich (``ja/nein``)
		 		 
         Zusatz:
            `k=ja` -  Ausgabe der Variationen in Kurzform
			
            `l=ja` - Ausgabe der  Variationen in Listenform
					 
            `f=ja` -  Formeln
			
            `b=ja` - Begriffe

   .. function:: auswahlen( ) 
				
         *k* - Auswahlen aus *n* Objekten (Übersicht)
		 
         Zusatz:  `a=ja` -  Algorithmus als Pseudocode			
			
   .. function:: zuf_zahl( bereich1  /[, bereich2, ... ]  /[, anzahl] ) 
   
         Erzeugung von ganzzahligen Pseudo-Zufallszahlen
		 
         Synonym: **zufZahl**
		 
         *bereich* :    Bereichsangabe  z.B. (0, 9);  [1, 6]
		 
         *anzahl* :    Anzahl der erzeugten Zahlen; Standard = 1
		 
         Zusatz: 
            `w=nein` - keine Wiederholung von Zahlen; Standard=ja
		 
            `s=ja` - sortierte Ausgabe mehrerer Zufallszahlen; Standard=nein
			
         Rückgabe:
            | eine einzelne Zahl oder eine Liste mit *anzahl* Elementen
            | ist die Anzahl der Bereiche > 1, so ist jedes Element ein
              Tupel, dessen *i*. Element aus dem *i*. Bereich ist   	
		
   .. function:: anzahl( daten /[, elem] )
		   
         Anzahl des Vorkommens eines Elementes in einer Liste / DatenReihe

         *daten* :   *Liste* von Elementen | *DatenReihe*
		 
         *elem* :     Listen- / Datenelement; bei Fehlen wird die Anzahl der 
         Elemente von *daten* zurückgegeben
		 
   *oder*
   
   .. function:: anzahl( elem )
   
         Es wird eine Funktion zurückgegeben, die die Anzahl des Vorkommens 
         des Elementes *elem* in einer Liste / DatenReihe zählt
		 
         | Bei deren Aufruf ist die Liste / DatenReihe als Argument anzugeben 
         | Ist *elem* selbst eine Liste, ist der Zusatz `el=ja` anzugeben		 

   .. function:: anzahl_treffer( treffer )
   
         Anzahl des Treffer

         Synonym: **anzahlTreffer** 
  
         *treffer* :    Element, das als Treffer / Erfolg angesehen wird 
         (etwa ``Wappen`` oder ``W`` beim Münzwurf)
		 
         Die Funktion ist nur als ZG-Funktion beim Erzeugen von 
         ZufallsGröße-Objekten verwendbar
		 
   .. function:: summe( daten )
     
        Summe der Elemente  einer Liste mit Daten / DatenReihe

        Synonyme:    **augen_summe**, **augenSumme**		
		
        *daten* :   *Liste* mit Daten | *DatenReihe*
		 
   .. function:: gesetze( )
     
        Einige Gesetze der Wahrscheinlichkeitsrechnung
		
   .. function:: loese(gleich /[, variable])
	   
   *oder*

   .. function:: loese(ungleich /[, variable])
			 
        Lösen von Gleichungen sowie von Ungleichungen
		
        *gleich* : linke Seite einer Gleichung der Form ``ausdruck = 0`` 
        oder Liste mit solchen Elementen (Gleichungssystem)
	
        *variable* : einzelne oder Liste von Variablen
		
        *ausdruck*: Ausdruck in den Variablen		
		
        *ungleich*:  Ungleichung der Form *ausdruck1* *rel* *ausdruck2*
		
        *rel* : Relation  < | <= | > | >=		
		
        Zusatz: `set=ja`   Verwendung von solveset; standardmäßig wird 
        solve verwendet (siehe SymPy-Dokumentation)		
		
   .. function:: einfach( objekt )

        Vereinfachung von Objekten

        *objekt* : Zahl | nummerischer Ausdruck | Vektor | Matrix

        Falls ``UMG.SIMPL`` gleich ``False`` ist, wird nicht vereinfacht
		 
        Zusatz: 
           `rad=ja` Einsatz von radsimp
		   
           `trig=ja`  Einsatz von trigsimp	

           `num=ja` Einsatz von nsimplify

           `sign=ja`  Einsatz von signsimp
		   
           (siehe SymPy-Dokumentation)		   
		  		 
   .. function:: ja_nein( ausdruck )

         Bewertung eines logischen Ausdruckes
	
         *ausdruck* : Ausdruck mit dem Wert ``True`` oder ``False``
		 
         Rückgabe:
            1 bei ``True``
			
            0 bei ``False``
 		  
   .. function:: stochastisch( objekt )

         Test auf stochastische(n) Vektor / Matrix
	
         *objekt* :   Vektor | Matrix
		 
         Ein Vektor ist stochastisch, wenn alle Komponenten in [0, 1] liegen		
         und ihre Summe 1 ist
		 
         Eine quadratische Matrix ist stochastisch, wenn alle Spaltenvektoren 
         stochastisch sind		
		
   |
   		
Mathematische Funktionen
------------------------
   
   .. function:: sqrt( x )
   
         (Quadrat-) Wurzel -  Funktion

         *x* : Zahl	

         Rückgabe einer reellen Zahl bei *x* > 0
		 
         Zusatz: `d=1` Dezimaldarstellung		 

   .. function:: exp( x )
   
         Exponential - Funktion   

         *x* : Zahl		

         Zusatz: `d=1` Dezimaldarstellung		 
		 
   .. function:: ln( x )
   
         Logarithmus - Funktion (natürlicher Logarithmus) 

         Synonym: **log**
		 
         *x* : Zahl		

         Rückgabe einer reellen Zahl bei *x* > 0
		 
         Zusatz: `d=1` Dezimaldarstellung		 

   .. function:: lg( x )
   
         Logarithmus - Funktion (dekadischer Logarithmus) 

         *x* : Zahl		

         Rückgabe einer reellen Zahl bei *x* > 0
		 
         Zusatz: `d=1` Dezimaldarstellung		 
		 
   .. function:: abs( x )
   
         Betrags - Funktion   

         *x* : Zahl		

         Zusatz: `d=1` Dezimaldarstellung		 
		 
   .. function:: sin( x )
   
         Sinus - Funktion (Winkel in Bogenmaß) 
		 
         *x* : Zahl		

         Zusatz: `d=1` Dezimaldarstellung		 
		 
   .. function:: arcsin( x )
   
         Arkussinus -Funktion (Winkel in Bogenmaß)   
		 
         Synonym: **asin**

         *x* : Zahl		

         Rückgabe einer reellen Zahl bei *x* :math:`\in [-1, 1]`
		 
         Zusatz: `d=1` Dezimaldarstellung		 
   
   .. function:: sing( x )
   
         Sinus - Funktion (Winkel in Grad) 
		 
         *x* : Zahl		

         Zusatz: `d=1` Dezimaldarstellung		 

   .. function:: arcsing( x )
   
         Arkussinus - Funktion (Winkel in Grad)   
		 
         Synonym: **asing**		 

         Rückgabe einer reellen Zahl bei *x* :math:`\in [-1, 1]`
		 
         *x* : Zahl		

         Zusatz: `d=1` Dezimaldarstellung		 

   .. function:: cos( x )
   
         Kosinus - Funktion (Winkel in Bogenmaß) 
		 
         *x* : Zahl		

         Zusatz: `d=1` Dezimaldarstellung		 

   .. function:: arccos( x )
   
         Arkuskosinus - Funktion (Winkel in Bogenmaß)   
		 
         Synonym: **acos**		 
   
         *x* : Zahl		

         Rückgabe einer reellen Zahl bei *x* :math:`\in [-1, 1]`
		 
         Zusatz: `d=1` Dezimaldarstellung		 
   
   .. function:: cosg( x )
   
         Kosinus - Funktion (Winkel in Grad) 
		 
         *x* : Zahl		
		 
         Zusatz: `d=1` Dezimaldarstellung		 
   		 
   .. function:: arccosg( x )
   
         Arkuskosinus - Funktion (Winkel in Grad)   
		 
         Synonym: **acosg**		 
   
         *x* : Zahl		

         Rückgabe einer reellen Zahl bei *x* :math:`\in [-1, 1]`
		 
         Zusatz: `d=1` Dezimaldarstellung		 
   
   .. function:: tan( x )
   
         Tangens - Funktion (Winkel in Bogenmaß) 
		 
         *x* : Zahl		
		 
         Zusatz: `d=1` Dezimaldarstellung		 
   
   .. function:: arctan( x )
   
         Arkustangens - Funktion (Winkel in Bogenmaß)   
		 
         Synonym: **atan**		 
   
         *x* : Zahl		
		 
         Zusatz: `d=1` Dezimaldarstellung		 
      
   .. function:: tang( x )
   
         Tangens  - Funktion (Winkel in Grad) 
		 
         *x* : Zahl		
		 
         Zusatz: `d=1` Dezimaldarstellung		 
   		 
   .. function:: arctang( x )
   
         Arkustangens - Funktion (Winkel in Grad)   
		 
         Synonym: **atang**		 
   
         *x* : Zahl		
   
         Zusatz: `d=1` Dezimaldarstellung		 
   
   .. function:: sinh( x )
   
         Sinus hyperbolikus - Funktion  
		    	
         *x* : Zahl		
   
         Zusatz: `d=1` Dezimaldarstellung		 
				
   .. function:: arsinh( x )
   
         Areasinus hyperbolikus - Funktion    
		 
         Synonym: **asinh**		 
      
         *x* : Zahl		
   
         Zusatz: `d=1` Dezimaldarstellung	
		 
   .. function:: cosh( x )
   
         Kosinus hyperbolikus  - Funktion  
		    		 
         *x* : Zahl		
   
         Zusatz: `d=1` Dezimaldarstellung	
		 
   .. function:: arcosh( x )
   
         Areakosinus hyperbolikus - Funktion    
		 
         Synonym: **acosh**		 
      
         *x* : Zahl		
   
         Zusatz: `d=1` Dezimaldarstellung	
		 
   .. function:: tanh( x )
   
         Tangens hyperbolikus - Funktion    
		    
         *x* : Zahl		
   
         Zusatz: `d=1` Dezimaldarstellung	
			
   .. function:: artanh( x ) 
   
         Areatangens hyperbolikus - Funktion    
		 
         Synonym: **atanh**		 
      
         *x* : Zahl		
   
         Zusatz: `d=1` Dezimaldarstellung	
	  
   .. function:: deg(winkel)
   
         Umrechnung Bogen- in Gradmaß   
		 
         Synonym: **grad**	
		 
         *winkel* : Winkel in Radian		 

         Rückgabe: *Winkel in Grad*		 
		 
         Zusatz: `d=n` Dezimaldarstellung mit *n* Kommastellen		 
   
   .. function:: rad(winkel)
   
         Umrechnung Grad- in Bogenmaß   
		 
         Synonym: **bog**		 
   
         *winkel* : Winkel in Grad		 
   
         Rückgabe: *Winkel in Radian*		 
   
         Zusatz: `d=n` Dezimaldarstellung mit *n* Kommastellen		 
      
   .. function:: kug_koord(punkt)
   
         Umrechnung in Kugelkoordinaten   
		 
         Synonym: **kugKoord**	

         *punkt* : Punkt der Einheitssphäre oder sPunkt	 
		 
         Rückgabe: *Länge, Breite*		 
   
         Zusatz: `g=1` Ausgaben in Grad		 
   
   .. function:: min(zahl1, zahl2, ...)
   
         Kleinste Zahl in einer Folge von zwei oder mehr Zahlen  
		 
         *zahl* : Zahl	 
		 
         Rückgabe: *kleinste Zahl*		 
   
   .. function:: max(zahl1, zahl2, ...)
   
         Größte Zahl in einer Folge von zwei oder mehr Zahlen  
		 
         *zahl* : Zahl	 
		 
         Rückgabe: *größte Zahl*		 
   
.. _konst:
		
   |
      
Konstanten
----------

   .. attribute:: pi 

         Zahl :math:`\pi` (3.1415...)
	  
   .. attribute:: E

         Eulersche Zahl :math:`e` (2.7182...)

   .. attribute:: I

         Imaginäre Einheit :math:`i`
	  
   .. attribute:: ja, nein, mit, ohne, Ja, Nein, Mit, Ohne

         Hilfsgrößen für True / False
	  
.. _sympy:
		
   |
   
SymPy - Funktionen
------------------

   .. function:: N(ausdruck, /[, m])
   
         Umwandlung von SymPy-Zahlen / -Ausdrücken in Dezimal-Zahlen 
         / -Ausdrücke  
		 
         *ausdruck* : nummerischer Ausdruck
		 
         *m* : Anzahl der Stellen	 

         Es kann auch die entsprechende **n**-Methode eines SymPy-Ausdruckes 
         verwendet werden: ``ausdruck.n(/[m])``
		 
   Weiterhin sind die SymPy-Funktionen **solve, solveset, expand, collect, 
   factor, simplify, nsimplify, radsimp, trigsimp, nsolve, re, im, diff**
   sowie die Klasse **Rational** direkt verwendbar
   
   Werden weitere SymPy-Elemente benötigt, können sie importiert werden
		
   |
   
.. warning::

   Die Namen **B, E, I, N** können überschrieben werden		
		
		
		