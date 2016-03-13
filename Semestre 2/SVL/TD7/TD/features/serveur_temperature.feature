Feature: transforming a temperature in celsius into en temperature in farhenheit

   As a user of the convertor
   I want to convert celcius into farhenheit
   Because I want to know the weather in Paris

   Scenario: the value is correctly displayed
      Given I am on the convertor page
      When I enter a celcius value and validate
      Then I can see the corresponding value in farhenheit

   @todo
   Scenario: the convertor refuses the wrong data
      Given I am on the convertor page
      When I enter a non floating value
      Then I can see an error message

   @todo
   Scenario: after conversion the convertor is still available

   @todo
   Scenario: after an error the convertor is still available
