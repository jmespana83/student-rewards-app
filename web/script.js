function loadJSON(callback) {

    var xobj = new XMLHttpRequest();
        xobj.overrideMimeType("application/json");
    xobj.open('GET', 'house_data.json', true);
    xobj.onreadystatechange = function () {
          if (xobj.readyState == 4 && xobj.status == "200") {
            // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
            callback(xobj.responseText);
          }
    };
    xobj.send(null);
 }

function init() {
 loadJSON(function(response) {
  // Parsing JSON string into object
    var actual_JSON = JSON.parse(response);
    console.log(actual_JSON);
 });
}

/**
 * Takes a javascript object modeled from house_results
 * and adds to #total table row.
 *
 * @param {Object} house
 */
const addTotalTableRow = (houseObj) => {

  // select <tbody> to add future new elements
  let totalTable = document.querySelector('#totals');
  let totalTbody = totalTable.querySelector('tbody');

  // create new HTML elements to insert and inject text in <td>
  let newRow = document.createElement('tr');
  let rowTitle = document.createElement('td');
  let rowTotal = document.createElement('td');

  // insert text for each new <td>
  rowTitle.innerText = houseObj.house;
  rowTotal.innerText = houseObj.total;

  // insert <td> into new <tr>
  newRow.appendChild(rowTitle);
  newRow.appendChild(rowTotal);

  // insert new row <tr> to #total table's <tbody>
  totalTbody.appendChild(newRow);
}

/**
 * Creates table with all student records on display
 * in their respective house
 *
 * @param {Object} house
 */
const createHouseTable = (houseObj) => {
  // destructure objects for easier variable naming
  let { house, total, students } = houseObj

  // select tbody within each house table by targeting <table> id's
  let table = document.querySelector(`#${house.toLowerCase()}`);
  let tbody = table.querySelector('tbody');
  let tfoot = table.querySelector('tfoot');

  // create new row for each students
  students.map(student => {
    // destructure
    const { name, points } = student;

    // create <tr> for each row
    let tr = document.createElement('tr');

    // create <td> for each field information
    let td_name = document.createElement('td');
    let td_points = document.createElement('td');

    // insert text into each <td>
    td_name.innerText = name;
    td_points.innerText = ;

    // insert <td> into each row, <tr>
    tr.appendChild(td_name);
    tr.appendChild(td_points);

    // append <tr> into <tbody>
    tbody.appendChild(tr);
  });

  // append total points to <tfoot>'s row after adding all students
  let td_total = document.createElement('td');
  // fill in final <td> cell with total
  td_total.innerText = total;
  // select row and insert last <td> of table
  let final_tr = tfoot.querySelector('tr');
  final_tr.append(td_total);
}

/**
 * Execute all DOM manipulation only when document is fully loaded.
 */
document.addEventListener('DOMContentLoaded', () => {

  // iterate through each house in JSON
  // data.map(house => {
  //   addTotalTableRow(house);
  //   createHouseTable(house);
  // });
});