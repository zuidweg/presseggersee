# presseggersee.nl

Website van de vakantiewoning Panorama Lodge (Pan 310) op EuroParcs Pressegger See, Karinthië.
Doel: promotie en extra boekingen, vooral in voor- en naseizoen.

## Opbouw
- `content.json`: alle teksten per taal (nl, de, en, it, pl). Teksten hier aanpassen.
- `build.py`: genereert de site naar `dist/`. Na elke wijziging: `python3 build.py`, dan `dist/` mee committen.
- `src/style.css`: opmaak. `src/img/`: foto's (worden naar `dist/img/` gekopieerd). Foto's per taal koppelen via `photos` in content.json (keys: hero, living, kitchen, terrace).
- Netlify publiceert `dist/` direct (zie netlify.toml), geen build-stap.
- `INDEXABLE` in build.py staat op False (noindex) tot de site definitief is.

## Afspraken
- Boekingen lopen via BookingExperts; elke taal heeft zijn eigen link (book_code in content.json).
- Geen verzonnen reviews of prijzen. Prijzen staan alleen in het boekingssysteem.
- Formulier `aanvraag` gaat via Netlify Forms.
