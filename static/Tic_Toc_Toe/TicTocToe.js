// restart game Button

var restart = document.querySelector('#b');

// clear Game

var squares = document.querySelectorAll('td');

// clear squares Function

function clearBoard{
  for (var i = 0; i < squares.length; i++){
    squares[i].textContent = '';
  }
}

restart.addEventListener('click', clearBoard)

// check the square changeMarker

function changeMarker(){
  if (this.textContent === ''){
    this.textContent = 'X';
  }else if (this.textContent === 'X'){
    this.textContent = '0';
  }else{
    this.textContent = '';
  }
}

for (var i = 0; i < squares.length; i++){
  squares[i].addEventListener('click', changeMarker)
}
