from deep_translator import GoogleTranslator
import polib

po_file = "locale/ar/LC_MESSAGES/django.po"
po = polib.pofile(po_file)

translator = GoogleTranslator(source="en", target="ar")

for entry in po:
    if not entry.msgstr:  # Only translate empty entries
        entry.msgstr = translator.translate(entry.msgid)
        print(f"Translated: {entry.msgid} -> {entry.msgstr}")

po.save()
print("Translation complete!")
