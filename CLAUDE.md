# presseggersee.nl

Website van de vakantiewoning Panorama Lodge (Pan 310) op EuroParcs Pressegger See, Karinthië.
Doel: promotie en extra boekingen, vooral in voor- en naseizoen.

## Opbouw
- `content.json`: alle teksten per taal (nl, de, en, it, pl). Teksten hier aanpassen.
- `build.py`: genereert de site naar `dist/`. Na elke wijziging: `python3 build.py`, dan `dist/` mee committen.
- `src/style.css`: opmaak. `src/img/`: foto's (worden naar `dist/img/` gekopieerd). Foto's per taal koppelen via `photos` in content.json (keys: hero, living, kitchen, terrace).
- GitHub Pages publiceert `dist/` via `.github/workflows/pages.yml` bij elke push naar main (repo is openbaar). Domein en DNS staan bij TransIP; `dist/CNAME` = presseggersee.nl.
- `INDEXABLE` in build.py: True = vindbaar in Google. Oude WordPress-URL's: `OLD_URLS` in build.py (doorstuurpagina's + 404.html met JS).

## Afspraken
- Boekingen lopen via BookingExperts; elke taal heeft zijn eigen link (book_code in content.json).
- Geen verzonnen reviews of prijzen. Prijzen staan alleen in het boekingssysteem.
- Formulier: `FORM_ENDPOINT` in build.py (FormSubmit AJAX). Leeg = formulier verborgen.
