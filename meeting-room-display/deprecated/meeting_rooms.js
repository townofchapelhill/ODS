var today;
var minute;
var hour;
var compare;
var org;
var start;
var end;
var end_;
var place;
var start_time = [];
var time;
var month;
var day_;
var month_;
var purpose;
var start;
var milt;
        
    $(document).ready( function() {
		
	tday=new Array("Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday");
	tmonth=new Array("January","February","March","April","May","June","July","August","September","October","November","December");

function GetClock(){
	var d=new Date();
	var nday=d.getDay(),nmonth=d.getMonth(),ndate=d.getDate(),nyear=d.getFullYear();
	var nhour=d.getHours(),nmin=d.getMinutes(),nsec=d.getSeconds(),ap;

	if(nhour==0){ap=" AM";nhour=12;}
		else if(nhour<12){ap=" AM";}
		else if(nhour==12){ap=" PM";}
		else if(nhour>12){ap=" PM";nhour-=12;}

		if(nmin<=9) nmin="0"+nmin;
		if(nsec<=9) nsec="0"+nsec;

document.getElementById('clockbox').innerHTML=""+tday[nday]+", "+tmonth[nmonth]+" "+ndate+", "+nyear+" "+nhour+":"+nmin+":"+nsec+ap+"";
}

	window.onload=function(){
	GetClock();
	setInterval(GetClock,1000);
	};

 setTimeout(function(){
      window.location.href = window.location.href;
  },(60000 * 30));

			today = new Date();
			month = today.getMonth() + 1;

			time  = today.getTime(); //results in milliseconds
        //to be used for the meetings that have ended within the past thirty minutes or will end later
        minute = today.getMinutes() - 30;
		if(minute < 0) {
			minute = Math.abs(today.getMinutes()-30);
			minute = 60 - minute;
			hour = today.getHours() - 1;
			compare = hour + ":"  + minute;
		} else {
 		hour = today.getHours();
		if(minute < 10) {
			minute = "0" + minute;
		}
		compare = hour + ":" + minute;
		}
		//test case default
		//compare = "00:00";
        updatePage(); 
		});
    
    function updatePage() {
   $.ajaxSetup({
        headers : {
           'Authorization' : 'Basic 30c2d9f2c74c92715b8bcd740d8f686d69a9d909d857331babb5f659'
        }
    });
   
$.getJSON("https://www.chapelhillopendata.org/api/records/1.0/search/?dataset=new_reservations" ,  function (jsonData)  {
     var count = 0;
    $.each(jsonData.records, function (object, objectData) {
		//MUST CONVERT TO MILITARY TIME TO CONVERT
	if(objectData.fields.start_time[1] === ':') {
		if(objectData.fields.start_time.slice(5) == 'AM') {
			start = "0" + objectData.fields.start_time.slice(0,4);
		} else if(objectData.fields.start_time.slice(5) == 'PM') {
			milt = parseInt(objectData.fields.start_time[0]) + 12;
			//adding the converted military time to the rest fo the string
			start = milt + ":" + objectData.fields.start_time.slice(2,4);
		}
	} else if(objectData.fields.start_time[2] === ':'){
		if(objectData.fields.start_time.slice(6) == 'AM') {
			start = objectData.fields.start_time.slice(0,5);
		} else if(objectData.fields.start_time.slice(6) == 'PM') {
			if(objectData.fields.start_time.slice(0,2) == '12'){
			start = objectData.fields.start_time.slice(0,5);
		}  else {
			milt = parseInt(objectData.fields.start_time.slice(0,2)) + 12;
			start = milt + ":" + objectData.fields.start_time.slice(3,5);
		}
		}	
	}	
        start_time[count] = start;
        count++;
        if(count == jsonData.records.length) {
            start_time.sort();
        }
    });

    var index;
	var accessed = [];
	var slicing;
	var stan;
	for(var x = 0; x < start_time.length; x++) {
		accessed[x] = false;
		slicing = start_time[x];
		if(parseInt(slicing) > parseInt("12:00") ) {
			//converting back from military time to standard time for camprisons
			stan = parseInt(slicing.slice(0,2)) - 12;
			start_time[x] = stan + ":" + slicing.slice(3);
		}
		if(slicing[0] == '0') {
			//getting rid of the added 0
			start_time[x] = slicing.slice(1,5);
		}
	}
	
    for(var  i = 0; i < start_time.length; i++) {
        for(var y = 0; y < jsonData.records.length; y++) {
            if(jsonData.records[y].fields.start_time.slice(0,5) == start_time[i] || jsonData.records[y].fields.start_time.slice(0,4) == start_time[i]) {
				if(accessed[y] === false) {
                index = y;
				accessed[y] = true;
				break;
				} 
			}
        }
		
		if(jsonData.records[index].fields.date[1] === '/') {
			month_ = parseInt(jsonData.records[index].fields.date[0]);
			if(jsonData.records[index].fields.date[3] === '/') {
				day_ = parseInt(jsonData.records[index].fields.date[2]);
			} else if(jsonData.records[index].fields.date[4] === '/' ) {
				//handles the case that the day is in double digits
				day_ = parseInt(jsonData.records[index].fields.date.slice(2,4));
			}
		} else if(jsonData.records[index].fields.date[2] === '/') {
			//handles the case if the month is in the double digits
			month_ = parseInt(jsonData.records[index].fields.date.slice(0,2));
			 if(jsonData.records[index].fields.date[4] === '/') {
				day_ = parseInt(jsonData.records[index].fields.date[3]);
			} else if(jsonData.records[index].fields.date[5] === '/' ) {
				//handles the case that the day is in double digits
				day_ = parseInt(jsonData.records[index].fields.date.slice(3,5));
			}
		}
		
		if(jsonData.records[index].fields.end_time[1] === ':') {
		if(jsonData.records[index].fields.end_time.slice(5) == 'AM') {
			end_ = "0" + jsonData.records[index].fields.end_time.slice(0,4);
		} else if(jsonData.records[index].fields.end_time.slice(5) == 'PM') {
			milt = parseInt(jsonData.records[index].fields.end_time[0]) + 12;
			//adding the converted military time to the rest fo the string
			end_ = milt + ":" + jsonData.records[index].fields.end_time.slice(2,4);
		}
	} else if(jsonData.records[index].fields.end_time[2] === ':'){
		if(jsonData.records[index].fields.end_time.slice(6) == 'AM') {
			end_ = jsonData.records[index].fields.end_time.slice(0,5);
		} else if(jsonData.records[index].fields.end_time.slice(6) == 'PM') {
			if(jsonData.records[index].fields.end_time.slice(0,2) == '12'){
			end_ = jsonData.records[index].fields.end_time.slice(0,5);
		}  else {
			milt = parseInt(jsonData.records[index].fields.end_time.slice(0,2)) + 12;
			end_ = milt + ":" + jsonData.records[index].fields.end_time.slice(3,5);
		}
		}	
	}

	
        if(parseInt(jsonData.records[index].fields.date.slice(4)) === today.getFullYear() && month_ === month && day_ === today.getDate() && end_.localeCompare(compare) > 0) {
                    
                    if(jsonData.records[index].fields.organization !== null) {
                        org = jsonData.records[index].fields.organization;
                    } else {
                        org = "N/A";
                    }
                    if(jsonData.records[index].fields.start_time !== null) {
							start = jsonData.records[index].fields.start_time;
                    } else {
                        start = "N/A";
                    }
                    if(jsonData.records[index].fields.end_time !==null) {
						end = jsonData.records[index].fields.end_time;
                    } else {
                        end = "N/A";
                    }
                    if(jsonData.records[index].fields.space_name !==null) {
                        place = jsonData.records[index].fields.space_name;
                    } else {
                        start = "N/A";
                    }
					if(jsonData.records[index].fields.purpose !== null) {
						purpose = jsonData.records[index].fields.purpose;
					} else {
						purpose = "N/A";
					}
                    $(".table").append("<tr><td>" + start + "</td><td>" + end + "</td><td>" + org + "</td><td>" + purpose +  "</td><td>" + place + "</td></tr>");
                }
    } 
});
        }
		
		