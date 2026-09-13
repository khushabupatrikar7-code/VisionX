import argostranslate.translate

text = "Hello, where is the nearest train station?"
translated = argostranslate.translate.translate(text, "en", "hi")
print(f"English: {text}")
print(f"Hindi: {translated}")