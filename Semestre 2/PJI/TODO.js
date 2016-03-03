// Test la connection internet

function CheckConnection()
{
     if( !navigator.network )
     {
         // set the parent windows navigator network object to the child window
         navigator.network = window.top.navigator.network;
     }

    // return the type of connection found
   return ( (navigator.network.connection.type === "none" || navigator.network.connection.type === null ||
          navigator.network.connection.type === "unknown" ) ? false : true );
}

// A rajouter dans le manifest
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.INTERNET" />

// recupère un webservice en ajax

$(document).ready(function() {
    $.ajax({
        url: "http://rest-service.guides.spring.io/greeting"
    }).then(function(data) {
       $('.greeting-id').append(data.id);
       $('.greeting-content').append(data.content);
    });
});
