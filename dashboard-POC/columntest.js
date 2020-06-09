/*global $*/
// initialize variables for interval of refreshing
var minutes = 60;
var milliseconds = min_to_ms(minutes);
var monthNames = ["January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"];
var d = new Date();
var currMonth = d.getMonth();
var currDay = d.getDay();
$('.currMonth').text(monthNames[currMonth]);


// function that converts minutes to milliseconds for use in update_interval function
function min_to_ms(min) {
    return min*60*1000;
}

// update permit data & transit data
function update_permits() {
    $.getJSON("https://www.chapelhillopendata.org/api/records/1.0/download/?dataset=permits&format=json&apikey=" + ODS_api + "&callback=?", function(today){
        // save counters and current date in variables
        var m_count = 0;
        var d_count = 0;
        var fm_count = 0;
        var fd_count = 0;
        var d = new Date();
        var current_month = d.getMonth() + 1;
        var current_year = d.getFullYear();
        var current_day = d.getDate();
        //alert(current_day + " day " +  current_month + " month " + current_year + " year ")
        // loop through data and increment counter accordingly
        for(var i = 0; i < today.length; i++) {
            try{
                var date = today[i].fields.issue_date.split('-');
                var file_date = today[i].fields.date_filed.split('-');
                
                if(date[1] == current_month && date[0] == current_year) {
                    m_count+=1;
                }
                if(date[1] == current_month && date[2] == current_day && date[0] == current_year) {
                    d_count+=1;
                }
                if(file_date[1] == current_month && file_date[0] == current_year) {
                    fm_count+=1;
                }
                if(file_date[1] == current_month && file_date[2] == current_day && file_date[0] == current_year) {
                    fd_count+=1;
                }
            }catch(e) {
                continue;
            }
        }
        
        $('#issuedMonth').text(m_count);
        $('#issuedToday').text(d_count);
        $('#filedMonth').text(fm_count);
        $('#filedToday').text(fd_count);
    });    
}

// update items info
function update_items() {
    var total_checked_out = 0;
    $.getJSON("https://www.chapelhillopendata.org/api/records/1.0/search/?dataset=overdue-items&rows=1&apikey=" + ODS_api + "&callback=?", function(od_items) {
        // add amount of overdue items to checked out items
        $.getJSON("https://www.chapelhillopendata.org/api/records/1.0/search/?dataset=checked-out-items&rows=1&apikey=" + ODS_api + "&callback=?", function(co_items) {
            total_checked_out = co_items.nhits+od_items.nhits;
            $('#checkedOut').text(total_checked_out);
            $.getJSON("https://www.chapelhillopendata.org/api/records/1.0/search/?dataset=library-items&rows=1&facet=status&refine.status=AVAILABLE&apikey=" + ODS_api + "&callback=?", function(total_a) {
                $('#percentOut').text((total_checked_out/total_a.nhits*100).toFixed(2));
            });
        });
    });
    // add active patrons
    $.getJSON("https://www.chapelhillopendata.org/api/records/1.0/search/?dataset=activepatrons&rows=1&apikey=" + ODS_api + "&callback=?", function(ap) {
        $('#activeP').text(ap.nhits);
    });
}

// update open data block
function update_od_police() {
    $.getJSON("https://www.chapelhillopendata.org/api/datasets/1.0/search?rows=1&apikey=" + ODS_api + "&callback=?", function(datasets){
        // set number of datasets
        $('#numD').text(datasets.nhits);
    });
    $.getJSON("https://www.chapelhillopendata.org/api/records/1.0/analyze/?dataset=ods-datasets-monitoring&source=monitoring&y.total_records.expr=records_count&y.total_records.func=SUM&apikey=" + ODS_api + "&callback=?", function(records){
        // set number of records total
        $('#numR').text(records[0].total_records);
    });
    $.getJSON("https://www.chapelhillopendata.org/api/records/1.0/analyze/?dataset=ods-api-monitoring&q=user_id:anonymous&source=monitoring&x=user_ip_addr&y.serie1.func=COUNT&apikey=" + ODS_api + "&callback=?", function(anon_users){
        $.getJSON("https://www.chapelhillopendata.org/api/records/1.0/analyze/?dataset=ods-api-monitoring&q=not+user_id:anonymous&source=monitoring&x=user_id&y.serie1.func=COUNT&apikey="  + ODS_api + "&callback=?", function(users){
        // set number of users total
        $('#numU').text(anon_users.length + users.length);
        });
        
        // update police info
        $('#hours').text(4528.5);
        $('#calls').text(7553);
    });
}

// update transit info
function update_transit() {
    $.getJSON("https://www.chapelhillopendata.org/api/records/1.0/search/?dataset=nextbuscount&rows=1&sort=route&facet=route&apikey=" + ODS_api + "&callback=?", function(active){
        $('#activeR').text(active.facet_groups[0].facets.length); 
    });
    
    $.getJSON("https://www.chapelhillopendata.org/api/records/1.0/search/?dataset=nextbuscount&rows=100&sort=route&apikey=" + ODS_api + "&callback=?", function(buses) {
        var totalSpeed = 0;
        $('#inService').text(buses.nhits);
        for(var i = 0; i < buses.records.length; i++){
            totalSpeed += buses.records[i].fields.speed_km_hr;
        }
        $('#avgSpeed').text((totalSpeed/buses.records.length)*0.6214);
    });
}

// update website data info
function update_site_data() {
    var variable;
    $.getJSON("https://www.chapelhillopendata.org/api/records/1.0/search/?dataset=daily-sessions-townofchapelhillorg&sort=column_2&apikey=" + ODS_api + "&callback=?", function(daily_sessions){
        // save amount of sessions today in variable
        variable = daily_sessions.records[0].fields.column_2;
        $('#sessionsToday').text(variable);
    });
    $.getJSON("https://www.chapelhillopendata.org/api/records/1.0/search/?dataset=monthly-sessions-townofchapelhillorg&sort=column_2&facet=column_1&facet=column_2&apikey=" + ODS_api + "&callback=?", function(monthly_sessions){
        // save amount of sessions this month in variable
        variable = monthly_sessions.records[0].fields.column_2;
        $('#sessionsMonth').text(variable);
    });
    $.getJSON("https://www.chapelhillopendata.org/api/records/1.0/search/?dataset=daily-searches-townofchapelhillorg&sort=column_2&facet=column_2&apikey=" + ODS_api + "&callback=?", function(daily_search){
        // save top searches today in variable
        variable = daily_search.records[0].fields.column_1;
        $('#topSearchToday').text(variable);
    });
    $.getJSON("https://www.chapelhillopendata.org/api/records/1.0/search/?dataset=monthly-searches-townofchapelhillorg&sort=column_2&facet=column_1&facet=column_2&apikey=" + ODS_api + "&callback=?", function(monthly_search){
        // save top searches this month in variable
        variable = monthly_search.records[0].fields.column_1;
        $('#topSearchMonth').text(variable);
    });
}

// function that gets a json and updates the page 
function update_page() {
    // gets local json file
    /*global $*/
    /*global ODS_api*/
    
    // update Permit and Transit info
    update_permits();
    
    // update items info
    update_items();
    
    // update Open Data info
    update_od_police();
    
    // update Transit info
    update_transit();
    
    // update website info
    update_site_data();
    
    // display updated date
    var d = new Date();
    var offset = -300;
    var estDate = new Date(d.getTime() + offset*60*1000);
    var uDate = estDate.toUTCString().replace('GMT', '');
    $('#stamp').text('Updated: ' + uDate + ' - Prototype - Revision 1');
}

// function that calls update_page every specified minutes
function update_interval(interval) {
    var update = setInterval(update_page, interval);
}

// call update_page to get the initial values
update_page();

// call update_interval to display the data and start timer
update_interval(milliseconds);