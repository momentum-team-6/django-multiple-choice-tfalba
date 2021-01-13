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
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

let correctAnswer = document.querySelector('.mark-answered')

if (correctAnswer != null) {
  let cardPk = correctAnswer.parentElement.dataset.cardPk
  let URL = `/decks/cards/${cardPk}/mark_answered`
  
  correctAnswer.addEventListener('click', e => {
    console.log("I'm here")
    console.log(cardPk)
    console.log(URL)
    fetch(URL, {
      headers:{
        'Accept': 'application/json/json',
        'X-Requested-With': 'XMLHttpRequest',
      },
    })
    .then(response => {
      return response.json()
    })
    .then(data => {
      console.log(data)
      // debugger
    })
  })
}
