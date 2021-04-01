<?php

$servername = "localhost";

// REPLACE with your Database name
$dbname = "WeatherStation";
// REPLACE with Database user
$username = "WeatherStation";
// REPLACE with Database user password
$password = "XXXX"; // TBD
 
// If you change this value, the API key in the sketch needs to match
$api_key_value = "YYYY"; // TBD

$api_key= $value = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $api_key = test_input($_POST["api_key"]);
    if($api_key == $api_key_value) {
        $value = test_input($_POST["value"]);
        
        // Create connection
        $conn = new mysqli($servername, $username, $password, $dbname);
        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        } 
        
        $sql = "INSERT INTO DayData (value)
        VALUES ('" . $value . "')";
        
        if ($conn->query($sql) === TRUE) {
            echo "New record created successfully";
        } 
        else {
            echo "Error: " . $sql . "<br>" . $conn->error;
        }
    
        $conn->close();
    }
    else {
        echo "Wrong API Key provided.";
    }

}
else {
    echo "No data posted with HTTP POST.";
}

function test_input($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}

?>