# meeting_room_scripts
A list of meeting room scripts for the Chapel Hill Open Data portal. Data is retrieved through an XML feed at http://kb.demcosoftware.com/article.php?id=720.

<strong>New Versions:</strong>

The updated scripts for the meeting room data now retrieve both future meeting room reservations and past meeting room reervations.  The script "updated_meetings.py" retrieves reservation data for up to 30 days into the future, the range can be extended as desired.

<strong>IMPORTANT NOTE</strong>

"aggregate_reservations.py" may accumulate all reservations for the last 144 days - the maximum that the API will permit.  The code is commented out for daily runs which append the previous day's reservations to the master CSV.

In the event that the master CSV is lost, uncomment the loop code to recreate it.
<pre>
for day in range(-143,0):
    get_reservations(day)
</pre>