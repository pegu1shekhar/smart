from clarifai.rest import ClarifaiApp

app = ClarifaiApp(api_key='a18d01b5adca4eca9413d7f9b228a391')

model = app.models.get('aaa03c23b3724a16a56b629203edc62c')

response = model.predict_by_url(
    url='https://www.elementstark.com/woocommerce-extension-demos/wp-content/uploads/sites/2/2016/12/pizza.jpg')

for temp in response['outputs'][0]['data']['concepts']:
    print temp