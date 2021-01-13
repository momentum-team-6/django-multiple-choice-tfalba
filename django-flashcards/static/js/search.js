console.log('Hello from top')

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue
}
const csrftoken = getCookie('csrftoken')

const actorSearchForm = document.querySelector('#movie-form-3')
const movieDisplay2 = document.querySelector('#display-2')
const dbActorPrefix = 'https://api.themoviedb.org/3/search/person?api_key=cdea2b0b411e1e124dcdfb6985b46497&query='
const posterPrefix = 'https://image.tmdb.org/t/p/w200'

actorSearchForm.addEventListener('submit', function (event) {
  event.preventDefault()
  const searchTerm = document.getElementById('actor-search').value
  console.log(searchTerm)
  searchActors(searchTerm)
})

// This will allow the choice to submit the card and run createMovie
movieDisplay2.addEventListener('click', function (event) {
  if (event.target.classList.contains('add-card')) {
    console.log('I clicked add-card')
    createMovie(event.target.parentElement)
    // write a function instead of createMovie that will populate
    event.target.parentElement.parentElement.classList.add('hide-me')
  }
})

function searchActors (searchTerm) {
  console.log('running searchMovies')
  movieDisplay2.innerHTML = ''
  // change the fetch url to be the actor prefix
  fetch(dbActorPrefix + encodeURI(searchTerm) + '&append_to_response=known_for')
    .then(res => res.json())
    .then(data => {
      for (const actor of data.results) {
        if (actor.profile_path !== null) {
          showActorResults(actor, movieDisplay2)
        }
      }
    })
}
// url should be a view that django will recognize
// something called is_ajax??
// change the following to create new card instances for flashcards

// url = 'decks/cards/add/<int:deck_pk>/'
// where use template literal for <int:deck_pk>

  // need to define the equivalent of correctAnswer for this page
  // place data-pk on the proper element with deckpk info

let deckPk = movieDisplay2.dataset.deckPk
//  let deckPk = correctAnswer.parentElement.dataset.deckPk
let URL = `/decks/cards/ajax_add/${deckPk}/`

// Need to not have URL defined twice -- move to separate js files

function createMovie (obj) {
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
      question_image: obj.previousElementSibling.firstElementChild.id,
    })
  })
    .then(res => res.json())
    .then(data => {
      console.log(data)
      // what goes in here instead of getMovies??
      // getMovies()
    })
}

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
