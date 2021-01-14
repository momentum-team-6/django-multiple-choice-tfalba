console.log('Hello from top')

function getCookie (name) {
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break;
      }
    }
  }
  return cookieValue
}
const csrftoken = getCookie('csrftoken')

let correctAnswer = document.querySelector('.mark-answered')

const keepGoing = document.querySelector('.return-to-deck')

if (correctAnswer != null) {
  const cardPk = correctAnswer.parentElement.dataset.cardPk
  const URL = `/decks/cards/${cardPk}/mark_answered`

  correctAnswer.addEventListener('click', e => {
    fetch(URL, {
      headers: {
        Accept: 'application/json/json',
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
      .then(response => {
        return response.json()
      })
      .then(data => {
      })
  })
}

if (keepGoing != null) {
  const cardPk = keepGoing.parentElement.dataset.cardPk
  const URL3 = `/decks/cards/${cardPk}/mark_keep_going`

  keepGoing.addEventListener('click', e => {
    fetch(URL3, {
      headers: {
        Accept: 'application/json/json',
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
      .then(response => {
        return response.json()
      })
      .then(data => {
      })
  })
}

const colorChoices = document.querySelectorAll('.color-choice')
for (const colorChoice of colorChoices) {
  if (colorChoice != null) {
    colorChoice.addEventListener('click', e => {
      const colorPk = colorChoice.dataset.colorPk
      const userPk = colorChoice.parentElement.dataset.userPk
      const URL2 = `/decks/${userPk}/color_choice/${colorPk}`

      fetch(URL2, {
        headers: {
          Accept: 'application/json/json',
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
        .then(response => {
          return response.json()
        })
        .then(data => {
          location.reload()
        })
    })
  }
}
