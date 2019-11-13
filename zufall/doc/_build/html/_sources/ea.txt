
EA - EreignisAlgebra
====================

.. currentmodule:: zufall.lib.objekte.ereignis_algebra

.. autoclass:: EreignisAlgebra

   **Eigenschaften und Methoden**
   
   .. autoattribute:: hilfe
   
         Synonym: **h**   
      
   .. autoattribute:: omega
      
   .. method:: berechnen(A, B, ausdruck )
   
         Berechnen von Ereignissen mittels Mengenalgebra 

         *A*, *B* : 
            Ereignisse (Teilmengen der Grundmenge als Liste/Tupel/
            Menge/Zeichenkette angegeben)		 
   
         *ausdruck* : zu berechnender Ausdruck in *A*, *B*; die Namen sind 
         zwingend
   
         Der Ausdruck wird nach den Regeln für logische Ausdrücke gebildet, 
         er ist immer als Zeichenkette einzugeben; als Operatoren werden 
         verwendet
		 
            ``nicht``, ``und``, ``oder``
			
         oder die entsprechenden englischen Wörter
		 
            ``not``, ``and``, ``or``
			
         Als Operanden dienen die Bezeichner *A* und *B*; sie beziehen sich 
         auf die ersten beiden Argumente (die eventuell andere Namen erhalten 
         hatten). Neben den damit erzeugbaren Ausdrücken sind folgende 
         erlaubt, sie sind exakt in der angeführten Form zu schreiben und 
         können auch als Operanden in anderen Ausdrücken dienen, wobei sie 
         hier in Klammern zu schreiben sind (statt *B* kann auch *A* stehen
         und umgekehrt)
		 
            ``gegen A`` (für das Gegenereignis)
			
            ``sowohl A als auch B``
			
            ``entweder A oder B``
			
            ``weder A noch B``
			
            ``mindestens A oder B``
			
            ``höchstens A oder B``
			
         Wird als Grundmenge das (große englische) Alphabet benutzt, 
         müssen *A* und *B* als Wörter (Zeichenketten oder Symbole)
         angegeben werden
			 
         Zusatz: 
            `t=ja` - Erläuterung mit Vier-Felder-Tafel
			
            `v=ja` - zusätzliche Erzeugung eines Venn-Diagramms
			
            `vt=ja` - alleinige Erzeugung der Vier-Felder-Tafel
			
            `ve=ja` - alleinige Erzeugung des Venn-Diagramms		 
			    
   .. method:: einordnen(A, B)
   
         Einordnen in eine Vier-Felder-Tafel   
		 
         *A*, *B* : 
            Ereignisse (Teilmengen der Grundmenge als Liste/Tupel/
            Menge/Zeichenkette angegeben; Grundlage für die 
            Vier-Felder-Tafel)	
			
            Wird als Grundmenge das (große englische) Alphabet 
            benutzt, müssen *A* und *B* als Wörter (Zeichenketten 
            oder Symbole) angegeben werden
		 
   
   .. method:: venn(A, B, ausdruck)
   
         Venn-Diagramm zur Darstellung der Verknüpfung von Ereignissen

         *A*, *B* : 
            Ereignisse (Teilmengen der Grundmenge) als Liste/Tupel/
            Menge/Zeichenkette angegeben
			
         *ausdruck* :  Ausdruck in *A*, *B*
			
         Näheres siehe bei der Methode berechnen		 
   
   .. method:: vt(A, B, ausdruck)
   
         Vier-Felder-Tafel-Diagramm zur Darstellung der Verknüpfung von 
         Ereignissen

         *A*, *B* : 
            Ereignisse (Teilmengen der Grundmenge) als Liste/Tupel/
            Menge/Zeichenkette angegeben
			
         *ausdruck* :  Ausdruck in *A*, *B*
			
         Näheres siehe bei der Methode berechnen		 

   .. method:: wort2menge(wort)
   
         Wort :math:`\rightarrow` Menge seiner Buchstaben 

         *wort* : Wort - Zeichenkette (in ' ' bzw. " ") oder Symbol
   
         Gebrauch bei einer Ereignisalgebra mit dem englischen
         Alphabet als Grundmenge			
   