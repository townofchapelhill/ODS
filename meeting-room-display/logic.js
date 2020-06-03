// Once document's ready, run script
$(document).ready(function getDate() {
    const prettyDate = moment().format('MMMM DD, YYYY');
    $("#header").append("<h3 id='title'>Meetings & Events for: " + prettyDate + "</h3>");
    getReservations();

    // Constructor to store reservation information
    function Reservation(time, orgName, desc, location, pubPriv, sorter) {
        this.duration = time,
        this.organization = orgName,
        this.description = desc,
        this.location = location,
        this.public = pubPriv,
        this.num = sorter
    };

    // function performs GET request to Open Data Soft endpoint
    function getReservations() {
        const apiDate = moment().format('MM%2FDD%2FYYYY')
        const apiQuery = "https://www.chapelhillopendata.org/api/records/1.0/search/?dataset=new_reservations&rows=25&facet=startdate&facet=enddate&facet=location&refine.startdate=" + apiDate + "&timezone=America%2FNew_York";

        $.ajax({
            url: apiQuery,
            method: "GET"
        }).done(function(response) {
            const reservationData = [];

            // Loop parses response and only stores desired entries
            for(var i = 0; i < response.records.length; i++) {
                // remove any "placeholder" reservations
                if (response.records[i].fields.description.includes('placeholder') || response.records[i].fields.description.includes('(placeholder)')) { 
                    continue;
                // only include entries for library meeting rooms
                } else if (response.records[i].fields.location === "Meeting Room B") {
                    reservationData.push(response.records[i].fields);
                } else if (response.records[i].fields.location === "Meeting Room C") {
                    reservationData.push(response.records[i].fields);
                } else if (response.records[i].fields.location === "Meeting Room D") {
                    reservationData.push(response.records[i].fields);
                } else if (response.records[i].fields.location === "Meeting Room A") {
                    reservationData.push(response.records[i].fields);
                } else {
                    continue
                }
            };
            // call next function
            parseData(reservationData);
        });
    };

    // parse data, organize chronogically and transform datetime values
    function parseData(reservations) {
        const objReservations = [];

        for (i = 0; i < reservations.length; i++) {
            // store transformed data in variables to be kept in objects
            let sorter = reservations[i].startdate.slice(11, 13);
            let parseStart = reservations[i].startdate.split("T");
            let dblParseStart = parseStart[1].split("-");
            const startTime = moment(dblParseStart[0], "HH:mm:ss").format("h:mm a");

            let parseEnd = reservations[i].enddate.split("T");
            let dblParseEnd = parseEnd[1].split("-");
            const endTime = moment(dblParseEnd[0], "HH:mm:ss").format("h:mm a");

            const formattedTime = startTime + " - " + endTime;
            
            // create new object for each iterate
            var newRes = new Reservation(formattedTime, '', reservations[i].description, reservations[i].location, '', sorter);
            objReservations.push(newRes);
        };

        // This sorts the list so it displays chronoligcally once appended
        objReservations.sort(function(a, b) {
            let a1 = a.num;
            let b1 = b.num;
            if (a1 === b1) {
                return 0;
            }
            return a1 > b1 ? 1 : -1;
        });

        // next function
        populateTable(objReservations);
    };

    // DOM manipulation to populate the table and include some dynamic styling
    function populateTable(reservations) {
        for (i = 0; i < reservations.length; i++) {
            // gives a different classname to the last row for styling purposes
            if (i === reservations.length - 1) {
                $('#table').append("<tr id='table-border'> <td class='table-section'>" + reservations[i].duration + "</td> <td class='table-section'>" + reservations[i].description + "</td> <td class='table-section'>" + reservations[i].location + "</td> <td class='table-section'>" + reservations[i].public + "</td> </tr>");
                continue
            };
            $('#table').append("<tr class='table-row'> <td class='table-section'>" + reservations[i].duration + "</td> <td class='table-section'><div class='table-description'>" + reservations[i].description + "</div></td> <td class='table-section'>" + reservations[i].location + "</td> <td class='table-section'>" + reservations[i].public + "</td> </tr>");
        };

        // dynaically creates a border that is shorter on top left & bottom right corners
        borderHeight = parseInt($('#table').height()) - 4;
        borderWidth = parseInt($('#table').width()) + 25;
        $('#border').css('height', borderHeight + 'px');
        $('#border').css('width', borderWidth + 'px');
    };

});