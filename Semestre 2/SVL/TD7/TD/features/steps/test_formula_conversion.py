import behave
import nose.tools
from calcul_temperature import *

@given('values in celsius and their equivalent in farhenheit')
def step_impl(context):
    pass

@then('with 100 Celsius I obtain a temperature of 212.0 Farhenheit')
def step_impl(context):
    nose.tools.assert_equal(celsius_to_farhenheit(100), 212.0)

@then('with 0 Celsius I obtain a temperature of 32.0 Farhenheit')
def step_impl(context):
    nose.tools.assert_equal(celsius_to_farhenheit(0), 32.0)
    
@then('with -1.5 Celsius I obtain a temperature of 29.3 Farhenheit')
def step_impl(context):
    nose.tools.assert_equal(celsius_to_farhenheit(-1.5), 29.3)
