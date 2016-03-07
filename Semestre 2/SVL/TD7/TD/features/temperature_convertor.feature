Feature: converting a temperature in Celsius into a temperature in Fahrenheit

    formula : F = C * 9 / 5 + 32

    Scenario Outline: temperature computations
    	Given values in celsius and their equivalent in farhenheit
	Then with <celsius> Celsius I obtain a temperature of <farhenheit> Farhenheit

    Examples: temperature values
    	| celsius | farhenheit |
	| 100	  | 212.0      |
	| 0	  | 32.0       |
	| -1.5	  | 29.3       |