Feature: calcul the ideal weight of a man or a woman

   As a user of the calculator
   I want to calcul my best weight
   Because I want to know my BMI

   Scenario: the value is correctly displayed
      Given I am on the calculator page
      When I enter my tall value and validate
      Then I can see my ideal weight value

   @todo
   Scenario: the calculator refuses the wrong data
      Given I am on the calculator page
      When I enter a non floating value
      Then I can see an error message

   @todo
   Scenario: after calculator the calculator is still available

   @todo
   Scenario: after an error the calculator is still available
