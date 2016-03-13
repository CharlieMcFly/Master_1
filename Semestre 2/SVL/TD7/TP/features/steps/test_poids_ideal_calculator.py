import behave
from selenium import webdriver
import nose.tools

@given('I am on the calculator page')
def step_impl(context):
    context.navigateur = webdriver.Firefox()
    context.navigateur.get('http://localhost:8080/temperature')

@when('I enter my tall and my sexevalue and validate')
def step_impl(context):
    input_box = context.navigateur.find_element_by_xpath("//input")
    input_box.send_keys("100")
    input_box.submit()

@then('I can see my ideal weight value')
def step_impl(context):
    message = context.navigateur.find_element_by_id('retour_poids_ideal')
    text = message.text
    context.navigateur.quit()
    nose.tools.assert_true("212.0" in text)
