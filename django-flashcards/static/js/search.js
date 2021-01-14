console.log('Hello from top')

const actorSearchForm = document.querySelector('#movie-form-3')
const searchResultDisplay = document.querySelector('#display-2')
const dbActorPrefix = 'https://api.themoviedb.org/3/search/person?api_key=cdea2b0b411e1e124dcdfb6985b46497&query='
const posterPrefix = 'https://image.tmdb.org/t/p/w200'

if (actorSearchForm != null) {
  /* ------------------------------------------------------------------------------------------------------------------ */
  /*                                  Event listeners for search and for submit result                                  */
  /* ------------------------------------------------------------------------------------------------------------------ */

  actorSearchForm.addEventListener('submit', function (event) {
    event.preventDefault()
    const searchTerm = document.getElementById('actor-search').value
    searchActors(searchTerm)
  })

  searchResultDisplay.addEventListener('click', function (event) {
    if (event.target.classList.contains('add-card')) {
      createCard(event.target.parentElement)
      event.target.parentElement.parentElement.classList.add('hide-me')
    }
  })

  function searchActors (searchTerm) {
    searchResultDisplay.innerHTML = ''
    fetch(dbActorPrefix + encodeURI(searchTerm) + '&append_to_response=known_for')
      .then(res => res.json())
      .then(data => {
        for (const actor of data.results) {
          if (actor.profile_path !== null) {
            showActorResults(actor, searchResultDisplay)
          }
        }
      })
  }

  /* ------------------------------------------------------------------------------------------------------------------ */
  /*                                             GET and POST fetch requests                                            */
  /* ------------------------------------------------------------------------------------------------------------------ */

  let deckPk = searchResultDisplay.dataset.deckPk
  let URL = `/decks/cards/ajax_add/${deckPk}/`

  function createCard (obj) {
    fetch(URL, {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({
        answer: obj.innerText,
        question_image: obj.previousElementSibling.firstElementChild.id
      })
    })
      .then(res => res.json())
      .then(data => {
        console.log(data)
        window.location.replace(`/decks/${deckPk}/`)
      })
  }

  /* ------------------------------------------------------------------------------------------------------------------ */
  /*                                             Rendering of search results                                            */
  /* ------------------------------------------------------------------------------------------------------------------ */

  function showActorResults (actor, display) {
    const actorMain = document.createElement('div')
    actorMain.classList.add('search-card')
    const actorName = document.createElement('div')
    const actorPoster = document.createElement('div')

    actorName.classList.add('actor-name')
    actorName.id = actor.id

    let posterUrl = ''
    if (actor.profile_path === null) {
      posterUrl = '/pexels-skitterphoto-390089.jpg'
    } else {
      posterUrl = posterPrefix + actor.profile_path
    }

    display.appendChild(actorMain)
    actorMain.appendChild(actorPoster)
    actorMain.appendChild(actorName)

    actorName.innerHTML = `${actor.name}<i class='fas fa-share-square add-card'></i></i>`
    actorPoster.innerHTML = `<img class='poster' id =${posterUrl} src=${posterUrl}></img>`
  }
}
