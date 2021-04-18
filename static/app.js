
particlesJS.load('particles-js', 'static/particles.json', function() {
  console.log('callback - particles-js config loaded');
});

function Hello(){
  let timePeriods = JSON.parse(periods)
  let availableCurrencies = JSON.parse(currencies)
  let indicators = JSON.parse(momentumIndicators)
  console.log(indicators.values())
  var indicatorElement = document.getElementById("indicators");
  var newRow = indicatorElement.insertRow(-1)
  index = indicatorElement.rows.length


  let options = ""

  for(var ind in indicators){
    console.log(indicators[ind])
    options = options + '<option value="' + indicators[ind] + '">' + indicators[ind] + '</option>'
  }
  let attempt = 
    '<tr> <td> <select name="' + index + '"> ' + options + '</select></td></tr>'
  newRow.innerHTML = attempt;
}