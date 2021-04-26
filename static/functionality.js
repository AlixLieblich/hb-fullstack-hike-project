'use strict';

// Display current weather data on trail detail pages

$.ajax({
    url: "https://community-open-weather-map.p.rapidapi.com/weather",
    headers: { 'x-rapidapi-key': "8e3f6010abmshc09fe5de80fba0ep138729jsn950d9f17b9e7", 
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"},
    data: {lat:  $('#current-weather').data("lat"), lon:$('#current-weather').data("lon")} 
}).done((res) =>{
        
        // let results = res['results'];
        let tempValue = res['main']['temp'];
        let nameValue = res['name']

        // console.log(res);
        // console.log(res.visibility);
        // console.log(tempValue)
        // console.log(nameValue)

        $('#current-weather').html(tempValue, nameValue);
    
    });

    // form

$({
    url: "/parks-by-state",
    data: {states: $("#state_name")}
})

function displayResults(results) {
    console.log(results)
    $('#db-search-results').html('')
    for (let i in resutls) {
        $('#db-search-results')
        .append(
            `<div>
                <input type="radio" name="chosen-item" value="${i}" required>
                ${results[i]}
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
    let formData = {'state_name': $('#state-select option:selected').val, 
                    'difficulty_select': $('#difficulty_select').val,
                    'park': $('#park').val};
    console.log(formData['state_name'])
    $.get('/process_search', formData, displayResults);
} )

