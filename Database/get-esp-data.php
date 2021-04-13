<?php

$servername = "localhost";

// REPLACE with your Database name
$dbname = "WeatherStation";
// REPLACE with Database user
$username = "WeatherStation";
// REPLACE with Database user password
$password = "XXXX"; // TBD

function StringInputCleaner($data) // NOTE: source https://www.digi77.com/ways-to-sanitize-data-and-prevent-sql-injections-in-php/
{
	//remove space bfore and after
	$data = trim($data);
	//remove slashes
	$data = stripslashes($data);
	$data = (filter_var($data, FILTER_SANITIZE_STRING));
	return $data;
}

if ($_SERVER["REQUEST_METHOD"] == "GET") {

	// Create connection
	$conn = new mysqli($servername, $username, $password, $dbname);
	// Check connection
	if ($conn->connect_error) {
		die("Connection failed: " . $conn->connect_error);
	}
	
	if ($_GET["selector"] == "0") {
		$sql = "select floor(avg(value)), reading_time, floor(timestampdiff(MINUTE, current_time(), reading_time) / 5) * 5 from DayData where reading_time >= timestampadd(DAY, -1, now()) group by floor(timestampdiff(MINUTE, current_time(), reading_time) / 5) * 5 order by reading_time desc";
		$filter = "floor(timestampdiff(MINUTE, current_time(), reading_time) / 5) * 5";
		$difference = 5;
	} elseif ($_GET["selector"] == "1") {
		$sql = "select floor(avg(value)), reading_time, floor(timestampdiff(MINUTE, current_time(), reading_time) / 35) * 35 from DayData where reading_time >= timestampadd(WEEK, -1, now()) group by floor(timestampdiff(MINUTE, current_time(), reading_time) / 35) * 35 order by reading_time desc";
		$filter = "floor(timestampdiff(MINUTE, current_time(), reading_time) / 35) * 35";
		$difference = 35;
	} elseif ($_GET["selector"] == "2") {
		$sql = "select floor(avg(value)), reading_time, floor(timestampdiff(MINUTE, current_time(), reading_time) / 155) * 155 from DayData where reading_time >= timestampadd(MONTH, -1, now()) group by floor(timestampdiff(MINUTE, current_time(), reading_time) / 155) * 155 order by reading_time desc";
		$filter = "floor(timestampdiff(MINUTE, current_time(), reading_time) / 155) * 155";
		$difference = 155;
	} elseif ($_GET["selector"] == "3") {
		$sql = "select floor(avg(value)), reading_time, floor(timestampdiff(MINUTE, current_time(), reading_time) / 1775) * 1775 from DayData where reading_time >= timestampadd(YEAR, -1, now()) group by floor(timestampdiff(MINUTE, current_time(), reading_time) / 1775) * 1775 order by reading_time desc";
		$filter = "floor(timestampdiff(MINUTE, current_time(), reading_time) / 1775) * 1775";
		$difference = 1775;
	}

	//$sql = "select id, reading_time, avg(value), floor(timestampdiff(MINUTE, current_time(), reading_time) / 60) * 60 from DayData group by floor(timestampdiff(MINUTE, current_time(), reading_time) / 60) * 60";

	$result = $conn->query($sql);
	//if ($result->num_rows > 0) {
		// output data of each row
		$check = 0;
		$row = mysqli_fetch_assoc($result);
		while ($check >= -(288 * $difference)) {
			if ($row[$filter] == $check) {
				echo StringInputCleaner($row["floor(avg(value))"]);
				$row = mysqli_fetch_assoc($result);
			}
			echo ",";
			$check = $check - $difference;
		}
		/*
		echo StringInputCleaner($row["floor(avg(value))"]);
		while ($row = mysqli_fetch_assoc($result)) {
			echo "," . StringInputCleaner($row["floor(avg(value))"]);
		}
		
	} else {
		echo "0 results";
	}*/
	$conn->close();
}
