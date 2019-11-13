.. _roulette_chancen

Ereignisse (Setzmöglichkeiten, Chancen) beim einmaligen Roulette-
Spiel

(Unbenannte) Ereignisse, die über die Menge der Zahlen angegeben 
werden:
                                               
Name                Beschreibung                                      Anzahl Zahlen Gewinnquote                                                                          
==================  ================================================= ============= ===========                                                    Zahlen      Gewinnquote         
plein               einzelne Zahl               z.B. 3 bzw. {3}         1           35 : 1
a_cheval            zwei angrenzende Zahlen     z.B. {13,16}            2           17 : 1
transversale_plein  Querreihe von drei Zahlen   z.B. {28,29,30}         3           11 : 1
carre               vier Zahlen, deren Felder   z.B. {14,15,17,18}      4            8 : 1
                    in einem Punkt zusammensto-  
                    ßen bzw. die ersten vier 
                    Zahlen 			
transversale_simple zwei benachbarte Querreihen z.B. {7,8 9,10,11,12}   6            5 : 1

Kolonne und Dutzend:
r.colonne1          die linke Reihe             {1,4,7,..,34}          12    2 : 1
r.colonne2          die mittlere Reihe          {2,5,8,..,35} 			 
r.colonne3          die rechte Reihe            {3,6,9,..,36}			
r.douze_premier     das erste Dutzend           {1,2,..,12}			 
r.douze_milieu      das mittlere Dutzend        {13,14,..,24}			
r.douze_dernier     das letzte Dutzend          {25,26,..,36}
			 
Einfache Chancen:
r.pair              die geraden Zahlen außer 0  {2,4,6,..,36}          18    1 : 1
r.impair            die ungeraden Zahlen        {1,3,5,..,35}			
r.rouge             die roten Zahlen            {1,3,7,..36}			
r.noir              die schwarzen Zahlen        {2,4,6,..35}			
r.manque            die erste Hälfte            {1,2,..,18}			
r.passe             die zweite Hälfte           {19,20,..,36}			
	""")
        return 

		
		
# 'Unbenannte' Chancen außer plein		
# --------------------------------		
_a_cheval = [{0, 1}, {0, 2}, {0, 3}, {1, 2}, {2, 3}, {1, 4}, {2, 5}, {4, 5}, {3, 6}, \
                  {5, 6}, {4, 7}, {5, 8}, {6, 9}, {7, 8}, {8, 9}, {7, 10}, {8, 11}, {10, 11}, \
                  {9, 12}, {11, 12}, {10, 13}, {11, 14}, {12, 15}, {13, 14}, {13, 16}, \
                  {14, 15}, {14, 17}, {15, 18}, {16, 17}, {17, 18}, {16, 19}, {17, 20}, \
                  {19, 20}, {18, 21}, {19, 22}, {20, 21}, {20, 23}, {22, 23}, {21, 24}, \
                  {22, 25}, {23, 24}, {23, 26}, {25, 26}, {24, 27}, {25, 28}, {26, 27}, \
                  {26, 29}, {28, 29}, {27, 30}, {28, 31}, {29, 30}, {29, 32}, {30, 33}, \
                  {31, 32}, {32, 33}, {31, 34}, {32, 35}, {33, 36}, {34, 35}, {35, 36}]		
_transversale_plein = [{1, 2, 3}, {4, 5, 6}, {7, 8, 9}, {10, 11, 12}, {13, 14, 15}, \
                  {16, 17, 18}, {19, 20, 21}, {22, 23, 24}, {25, 26, 27}, {28, 29, 30}, \
                  {31, 32, 33}, {34, 35, 36}]	
_carre = [{1, 2, 3, 4}, {1, 2, 4, 5}, {2, 3, 5, 6}, {4, 5, 7, 8}, {5, 6, 8, 9}, \
                  {7, 8, 10, 11}, {8, 9, 11, 12}, {10, 11, 13, 14}, {11, 12, 14, 15}, \
                  {13, 14, 16, 17}, {14, 15, 17, 18}, {16, 17, 19, 20}, {17, 18, 20, 21}, 
                  {19, 20, 22, 23}, {20, 21, 23, 24}, {22, 23, 25, 26}, {23, 24, 26, 27}, \
                  {25, 26, 28, 29}, {26, 27, 29, 30}, {28, 29, 31, 32}, {29, 30, 32, 33}, \
                  {31, 32, 34, 35}, {32, 33, 35, 36}]				  
_transversale_simple = [{1, 2, 3, 4, 5, 6}, {4, 5, 6, 7, 8, 9}, {7, 8, 9, 10, 11, 12}, \
                  {10, 11, 12, 13, 14, 15}, {13, 14, 15, 16, 17, 18}, {16, 17, 18, 19, 20, 21}, \
                  {19, 20, 21, 22, 23, 24}, {22, 23, 24, 25, 26, 27}, {25, 26, 27, 28, 29, 30}, \
                  {28, 29, 30, 31, 32, 33}, {31, 32, 33, 34, 35, 36}]				  
		
	
