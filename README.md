# texviper

## Dokumentaatio

[Vaatimusmäärittely](dokumentaatio/vaatimusmaarittely.md)

[Arkkitehtuurikuvaus](dokumentaatio/arkkitehtuuri.md)

[Työtuntikirjanpito](dokumentaatio/tuntikirjanpito.md)

## Asennus

Riippuvuudet asennetaan komennolla

```shell
poetry install
```

## Käyttö

### Käynnistys

Sovellus käynnistetään seuraavalla komennolla

```shell
poetry run invoke start
```

### Testaus

Testit voi suorittaa komennolla

```shell
poetry run invoke test
```

### Testikattavuus

Testikattavuusraportin voi luoda komennolla

```shell
poetry run invoke coverage-report
```

Raportti generoidaan projektin juureen htmlcov-hakemistoon.

### Lint

Lintterin voi suorittaa komennolla

```shell
poetry run invoke lint
```

### Clean

Generoidut raportit voi poistaa komennolla

```shell
poetry run invoke clean
```
