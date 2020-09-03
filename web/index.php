<?php
/**
 *  PHP view file – A mix of PHP and HTML code to produce a view of Database results
 */

// DB CONNECTION GOES HERE. No quotes around arguments like python config, but they do have to go immediately after
// the '=' sign separated by spaces.
$conn = pg_connect("host=salt.db.elephantsql.com dbname=rpnrceuz user=rpnrceuz password=trxpcf3NlLg-6X6oHYbwgKPYFGI3sO_n");
$gryffindor = pg_query($conn, "SELECT * FROM students WHERE house='Gryffindor'");
$slytherin = pg_query($conn, "SELECT * FROM students WHERE house='Slytherin'");
$ravenclaw = pg_query($conn, "SELECT * FROM students WHERE house='Ravenclaw'");
$hufflepuff = pg_query($conn, "SELECT * FROM students WHERE house='Hufflepuff'");

// store in query array to run parallel with house_list
$house_data = [$gryffindor, $slytherin, $ravenclaw, $hufflepuff];

// data structure for displaying tables
$house_list = [
    [
        'house' => 'Gryffindor',
        'total' => 0,
        'students' => []
    ],
    [
        'house' => 'Slytherin',
        'total' => 0,
        'students' => []
    ],
    [
        'house' => 'Ravenclaw',
        'total' => 0,
        'students' => []
    ],
    [
        'house' => 'Hufflepuff',
        'total' => 0,
        'students' => []
    ]
];

// loop through both arrays to combine data
for ($i = 0; $i < 4; $i++) {
    // go through each database fetch and fill in one house at a time
    while ($record = pg_fetch_row($house_data[$i])) {
        // store name and points and add to students array for each house
        array_push($house_list[$i]['students'], Array(
            'name' => $record[2],
            'points' => $record[4]
        ));
        $house_list[$i]['total'] += $record[4];                // add points to house total
    }
    // sort students by points in descending order for each house
    $points = array_column($house_list[$i]['students'], 'points');
    array_multisort($points, SORT_DESC, $house_list[$i]['students']);
}

// sort houses greatest to least points
$houses = array_column($house_list, 'total');
array_multisort($houses, SORT_DESC, $house_list);

?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Tigers Houses!</title>
    <link rel="stylesheet" href="bootstrap.min.css">
    <link rel="stylesheet" href="styles.css">
</head>

<body>
<div id="background-layer">
    <div id="main-container">
        <h1 class="text-center">Tiger Houses Results!</h1>
        <div>
            <h2 class="text-center">Current House Standings</h2>
            <table id="totals">
                <thead>
                <th>House</th>
                <th>Points</th>
                </thead>
                <tbody>
                <?php
                foreach ($house_list as $house) {
                    echo "<tr><td>" . $house['house'] . "</td><td>" . $house['total'] . "</td></tr>\n";
                }
                ?>
                </tbody>
            </table>
        </div>

        <?php
        // loop throu
        foreach ($house_list as $house) {
            echo <<< EOL
                <div class="house" >
                    <h3 class="text-center" > {$house["house"]} Standings </h3 >
                    <table id ="{$house["house"]}" >
                        <thead >
                            <tr >
                                <th >Name</th >
                                <th >Points</th >
                            </tr >
                        </thead >
                        <tbody >
                EOL;

                foreach($house['students'] as $student) {
                    echo "<tr><td>" . $student['name'] . "</td><td>" . $student['points'] . "</td></tr>\n";
                }

                echo <<< EOL
                        </tbody >
                        <tfoot >
                            <tr >
                                <td > 
                                    Total Points:
                                </td >
                                <td>
                                    {$house["total"]}
                                </td>
                            </tr >
                        </tfoot >
                    </table >
                </div >
                EOL;
        }
        ?>
    </div>
    <script src="https://code.jquery.com/jquery-3.4.1.min.js"
            integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>
    <script type="text/javascript" src="../house_results.json"></script>
    <script type="text/javascript" src="script.js"></script>
</div>
</body>
</html>
