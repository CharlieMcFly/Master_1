Feature: calculate the ideal weight of a man or a woman

    formule_for_men : W = T * 100 - 100 - (T * 100 - 150) / 4
    formule_for_women : W = T * 100 - 100 - (T * 100 - 150) / 2.5

    Scenario Outline: weight computations
      Given tall and sexe value  and their ideal weight
	    Then with <tall> Tall and <sexe> Sexe I obtain weight <weight> ideal weight

    Examples: weight values
    	| tall    | sexe  | weight     |
	    | 1.81	  | homme | 73.25      |
	    | 1.69    | femme | 61.4       |
