# Vaatimusmäärittely

## Käyttötarkoitus

Kyseessä on Latex-editori, jolla voidaan helposti luoda ja muokata Latex-dokumentteja. Sovelluksessa voi luoda projekteja, joissa dokumentteja voi muokata. Sovellus hallinnoi projektit tiedostojärjestelmässä käyttäjän puolesta, joten projekteja on helppo muokata ja ylläpitääm vaikka ne koostuisivat useista tiedostoista. Lisäksi sovellus mahdollistaa projektikohtaisten asetusten määrittelyn.

## Käyttäjäroolit
Sovelluksessa on yksi käyttäjärooli eli tavallinen käyttäjä. Käyttäjä hallinnoi sovellusta,
ja käyttäjällä on oikeus suorittaa kaikki sovelluksen mahdollistamat toiminnot. Erillistä ylläpitäjän roolia ei siis ole.

## Käyttöliittymä

Sovellus tarjoaa graafisen käyttöliittymän, joka muodostuu seuraavista näkymistä:

* Kotinäkymä: listaus olemassaolevista projekteista sekä uusien projektien luonti
* Projektinäkymä: aktiivisen projektin editori- ja esikatselupaneeli, muut avoimet projektit välilehtinä
* Asetukset: sovelluskohtaiset asetukset, kuten teema jne.
* Mallit: olemassaolevat mallit sekä mallien hallunta

Sovellus mahdollistaa useamman projektin avaamisen välilehtiin. Lisäksi projektin sisällä voi olla välilehdissä useampia lähdekooditiedostoja.

Allaoleva kuva havainnollistaa karkeasti sovelluksen näkymiä ja navigaatiota niiden välillä.

<img src="img/ui_kuvaus.svg" >

## Toiminnallisuus

### Sovelluksen avauduttua

* käyttäjä voi luoda uuden projektin
* käyttäjä voi tarkastella olemassaolevia projekteja
* käyttäjä voi avata olemassaolevan projektin
* käyttjä voi poistaa olemassaolevan projektin

### Projektin luominen

* projektin luomisen yhteydessä käyttäjä voi valita templaten, jota projektiin luodaan automaattisesti templaten määrittelemä oletustiedosto

### Projekti

* käyttäjä voi muokata Latex-lähdekoodia
* käyttäjä voi lisätä tai poistaa Latex-lähdekooditiedostoja
* käyttäjän ajaessa projektin sovellus päivittää esikatselunäkymän automaattisesti

### Sovellusasetukset

* käyttäjä voi luoda, muokata ja poistaa malleja, joita käytetään uuden projektin alustuksessa
* käyttäjä voi määrittää projektien oletustallennuspaikan
* käyttäjä voi määrittää tietokannan sijainnin ja nimen
* Teeman kustomointi: käyttäjä voi määrittää asetuksissa ulkoasun värit sekä fontin

## Jatkokehitysmahdollisuuksia

* Paketinhallinta: käyttäjä voi ladata latex-paketteja sovelluksen kautta suoraan repositoryista ilman manuaalista asennusta
* Koodin väritys
