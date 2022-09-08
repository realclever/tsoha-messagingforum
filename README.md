# tsoha-messagingforum

Keskustelusovellus

Sovelluksessa näkyy keskustelualueita, joista jokaisella on tietty aihe. Alueilla on keskusteluketjuja, jotka muodostuvat viesteistä. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

Keskustelusovellusta voi testata luomalla käyttäjätunnukset ja normaaleja ketjuja voi lukea myös ilman niitä.

Testausta varten on luotu käyttäjätunnukset user (pw: user) ja admin (pw:admin)

[Heroku](https://tsoha-messagingforum.herokuapp.com/)

Sovelluksen ominaisuuksia:

* __Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.__
* __Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän ja viimeksi lähetetyn viestin ajankohdan.__
* __Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.__
* __Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.__
* __Käyttäjä voi muokata lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin.__
* __Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.__
* __Ylläpitäjä voi lisätä ja poistaa keskustelualueita.__
* __Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.__
