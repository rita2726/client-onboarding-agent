import google.generativeai as genai

genai.configure(api_key="AIzaSyB_nGht2c0CNNwG2GYV75RLtYh5o0zWZa4")

models = genai.list_models()

for model in models:
    print(model.name, model.supported_generation_methods)
