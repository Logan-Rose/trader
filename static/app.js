
particlesJS.load('particles-js', 'static/particles.json', function() {
  console.log('callback - particles-js config loaded');
});

function Hello(){
  let timePeriods = JSON.parse(periods)
  let availableCurrencies = JSON.parse(currencies)
  let indicators = JSON.parse(momentumIndicators)

  var indicatorElement = document.getElementById("indicators");
  var newRow = indicatorElement.insertRow(-1)
  index = indicatorElement.rows.length -3


  let options = ""

  for(var ind in indicators){
    options = options + '<option value="' + ind + '">' + ind + '</option>'
  }

  let attempt = 
    '<tr> <td> <select name="' + index + '"> ' + options + '</select></td>' + 
    '<td><input type="number" id="buy_' + index + '" value="0" name="buy_' + index + '"></td>' +
    '<td><input type="number" id="sell_' + index + '" value="0" name="sell_' + index + '"></td> </tr>'
  
  newRow.innerHTML = attempt;
  let old = '<td> <select name="coinTwo"> </select> </td> <td> <select name="coinTwo"> </select> </td> <td> <select name="coinTwo"> </select> </td>'
}