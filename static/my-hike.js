'use strict';

function getHike(results) {
    $("#weather-info").html(results.hike);
}

function showForecast(evt) {
    evt.preventDefault();

    let url = "/hikes.json";
    let formData = {"trail_type": $("#trail_type-field").val()};

    $.get(url, formData, getHike);
}

$("#trail_type-field-form").on('submit', showForecast);

// unsuccessful attempted practice from skills assessment 4 to connect js file to html

// var el = document.querySelector("#login-button");
// console.log(el);
// console.log('#login-button');
// //collect hike info form Hiker API
// document.querySelector('#login-button').addEventListener('click', (evt) => {
//     const loginBtn = evt.target;
//     console.log(evt.target);
  
//     if (loginBtn.innerHTML === 'Log In') {
//       loginBtn.innerHTML = 'Log Out';
//     } else {
//       loginBtn.innerHTML = 'Log In';
//     }
// });

// unsuccessful attempted practice to get hike names from hike api

// let url = "https://www.benbrougher.tech/hiker/v1/trails/"
// let formData = {"name": $(url['trails']).val()};
// console.log("HOWDY")
// $.get(url, forData, (res) => {
//     const hikeNames = [];
//     for (const name of res.results) {
//         hikeNames.push(hike.name);
//     }
//     console.log("HERE")
//     console.log(hikeNames)
//     $('#hikes').append(hikeNames.join(', '));
// });