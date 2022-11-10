const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

var elements = document.getElementsByClassName("move-btn");

var myFunction = function() {
    var move = this.getAttribute("data-move");
    var pokemon = document.getElementById('pokemon').getAttribute('data-poke')
    var oppPoke = document.getElementById('opp-poke').getAttribute('data-opp')
    console.log(move, pokemon, oppPoke)
    
};

for (var i = 0; i < elements.length; i++) {
    elements[i].addEventListener('click', myFunction, false);
}
