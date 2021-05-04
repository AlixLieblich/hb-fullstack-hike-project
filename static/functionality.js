'use strict';

// Display current weather data on trail detail pages
let num=5;
let numm=10
let nummm=10/5
console.log(nummm)
$.ajax({
    url: "http://api.openweathermap.org/data/2.5/weather",
    data: {'appid': "", 
        lat:  $('#current-weather').data("lat"), 
        lon:$('#current-weather').data("lon")} 
}).done((res) =>{
        
        // let results = res['results'];
        let tempValue = res['main']['temp'];
        let tempValueFar = ((9/5)*(tempValue-273)+32);
        let temp = Math.round(tempValueFar)
        console.log("Far:")
        console.log(temp)
        let nameValue = res['name'];

        // console.log(res);
        // console.log(res.visibility);
        // console.log(tempValue)
        // console.log(nameValue)

        $('#current-weather').html(temp, nameValue);
    
    });

    // form

$({
    url: "/parks-by-state",
    data: {states: $("#state_name")}
})

function displayResults(results) {
    console.log('results:')
    console.log(results)
    $('#db-search-results').html('')
    for (let i in results) {
        $('#db-search-results').append(
            `<div>
                <input type="radio" name="chosen-item" value="${i}" required>
                ${results[i]['park']}
            </div>`
        );
    }
}
// // Update search form based on selected state
// $('#state-select').on('change', (evt) => {
//     evt.preventDefault();
//     let selectedOption = $(evt.target);
//     $('.state-specific').val('');
//     if ($('#state-select').val() === '') {

//     }
// })

$('.choice').on('change', (evt) => {
    console.log("sun apr 25")
    evt.preventDefault();
    let formData = {'state_name': $('#state-select option:selected').val(), 
                    'difficulty_select': $('#difficulty_select').val(),
                    'park': $('#park').val()};
    console.log(formData['difficulty_select'])
    $.get('/process_search', formData, displayResults);
    console.log("15:57")
    console.log(difficulty_select)
} )



