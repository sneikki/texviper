# texviper

## Dokumentaatio

[Vaatimusmäärittely](dokumentaatio/vaatimusmaarittely.md)

[Työtuntikirjanpito](dokumentaatio/tuntikirjanpito.md)

## Käyttö

Sovellus käynnistetään seuraavalla komennolla:

```shell
poetry run invoke start
```

Testit voi suoritaa komennolla:

```shell
poetry run invoke test
```

Testikattavuutta voi tutkia komennolla

```shell
poetry run coverage
```

Testikattavuusraportin voi luoda komennolla

```shell
poetry run coverage-report
```

Raportti generoidaan projektin juureen htmlcov-kansioon.
