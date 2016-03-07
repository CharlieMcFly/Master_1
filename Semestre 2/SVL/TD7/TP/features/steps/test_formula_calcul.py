import behave
import nose.tools
from poids_ideal import *

@given('tall value and their ideal weight')
def step_impl(context):
    pass

@then('with 1.81 Tall I obtain weight 73.25 ideal weight')
def step_impl(context):
    nose.tools.assert_equal(calculer_poids_ideal(1.81, 'homme'), 73.25)

@then('with 1.81 Tall I obtain weight 73.25 ideal weight')
def step_impl(context):
    nose.tools.assert_equal(celsius_to_farhenheit(0), 32.0)

@then('with 1.81 Tall I obtain weight 73.25 ideal weight')
def step_impl(context):
    nose.tools.assert_equal(celsius_to_farhenheit(-1.5), 29.3)
