'use strict';

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

// function displayResultsTwo(results) {
//     console.log('results2:')
//     console.log(results)
//     $('#db-search-trails-results').html('')
//     for (let i in results) {
//         $('#db-search-trail-results').append(
//             `<div>
//                 <input type="radio" name="chosen-item" value="${i}" required>
//                 ${results[i]['park']}
//             </div>`
//         );
//     }
// }
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
} )

// $('.chosen-item').on('click', (evt) => {
//     console.log("sat may 1")
//     evt.preventDefault();
//     let formData = {'state_name': $('#state-select option:selected').val(), 
//                     'difficulty_select': $('#difficulty_select').val(),
//                     'park': $('#park').val()};
//     console.log('/process_search_two', formData, displayResultsTwo);
//     console.log('did this work?')
// })






