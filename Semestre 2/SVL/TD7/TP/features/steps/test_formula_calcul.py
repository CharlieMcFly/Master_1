import behave
import nose.tools
from poids_ideal import *

@given('tall value and their ideal weight')
def step_impl(context):
    pass

@then('with 1.81 Tall and homme Sexe I obtain weight 73.25 ideal weight')
def step_impl(context):
    nose.tools.assert_equal(calculer_poids_ideal(1.81, 'homme'), 73.25)

@then('with 1.69 Tall and femme Sexe I obtain weight 61.4 ideal weight')
def step_impl(context):
    nose.tools.assert_equal(calculer_poids_ideal(1.69, 'femme'), 61.4)
