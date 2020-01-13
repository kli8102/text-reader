import os
from flask import Flask, flash, redirect, url_for, request, render_template, \
send_from_directory, safe_join
from werkzeug.utils import secure_filename

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
from spellchecker import SpellChecker

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
#from autocorrect import Speller

#checker = Speller(lang='en')

# file = input("Input a file: ")

def ocr_core(filename):
    try:

        im = Image.open(filename)
        print(filename)
        text = pytesseract.image_to_string(im)
        if text == "":
            print("No text or image cannot be uploaded")

        target = os.path.join(APP_ROOT, 'images/')
        if not os.path.isdir(target):
            os.mkdir(target)

        fn = secure_filename(filename.filename)
        destination = '/'.join([target, fn])
        im.save(destination)
    except Exception as e:
        print(e)
        return ""
    return text

# extracted = ocr_core(file)

def spell_check(extracted):
    checker = SpellChecker()
    words = extracted.split()

    alternatives = {}
    for word in words:
        if not word in alternatives and checker.correction(word) != word:
            alternatives[word] = checker.candidates(word)

    return alternatives


# print(extracted)
# spell_check(extracted)
