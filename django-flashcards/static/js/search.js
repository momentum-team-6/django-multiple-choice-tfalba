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
    console.log(searchTerm)
    searchActors(searchTerm)
  })

  // This will allow the choice to submit the card and run createMovie
  searchResultDisplay.addEventListener('click', function (event) {
    if (event.target.classList.contains('add-card')) {
      console.log('I clicked add-card')
      createMovie(event.target.parentElement)
      // write a function instead of createMovie that will populate
      event.target.parentElement.parentElement.classList.add('hide-me')
      console.log(event.target.parentElement.previousElementSibling.firstElementChild.id)
    }
  })

  function searchActors (searchTerm) {
    console.log('running searchMovies')
    searchResultDisplay.innerHTML = ''
    // change the fetch url to be the actor prefix
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

  function createMovie (obj) {
    console.log(obj.innerText)
    console.log(obj.previousElementSibling.firstElementChild.id)
    console.log(URL)
    console.log(deckPk)
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
        // what goes in here instead of getMovies??
        // getMovies()
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
