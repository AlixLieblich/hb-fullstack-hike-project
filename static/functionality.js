'use strict';

// Display current weather data on trail detail pages
console.log("howdy");
$('#test').html("from js, hello love");

// const lat = $('#current-weather').data("lat");
// const lon = $('#current-weather').data("lon");
$.ajax({
    url: "https://community-open-weather-map.p.rapidapi.com/weather",
    headers: { 'x-rapidapi-key': "8e3f6010abmshc09fe5de80fba0ep138729jsn950d9f17b9e7", 
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"},
    data: {lat:  $('#current-weather').data("lat"), lon:$('#current-weather').data("lon")} 
}).done((res) =>{
        // let results = res['results'];
        let tempValue = res['main']['temp'];
        let nameValue = res['name']

        console.log(res);
        console.log(res.visibility);
        console.log(tempValue)
        console.log(nameValue)

        $('#current-weather').html(tempValue);
    
    });

// let url = ;


// const key = "8e3f6010abmshc09fe5de80fba0ep138729jsn950d9f17b9e7"
// console.log(lat);
// console.log(lon);


// const querystring= {lat:`${lat}`, lon:`${lon}`};
// console.log(querystring);
// // let latLonData = {
// //                   "lat": , 
// //                   "lon": 
// //                   };
// //                   Uncaught TypeError: $(...).attr(...).value is not a function
// //                   at functionality.js:7

// $.get(url, querystring, (res) =>{
//     let results = res['results']
//     console.log("HIIIIIIIIIIIIIIIIIIIIIIIIIIIIII");
//     $('#current-weather').html(results);

// });