var unitedStates = {lat: 37.09024, lng: -95.712891};

var map = new google.maps.Map(document.getElementById("map"), {
    center: unitedStates,
    zoom: 5,
});

var cali = {lat: 36.778261, lng: -119.4179324};
var marker = new google.maps.Marker({
    position: cali,
    map: map,
    title: "Cali"

});
