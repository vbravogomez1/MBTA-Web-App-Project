from flask import Flask, request, render_template
import mbta_helper


app = Flask(__name__)


@app.route("/")
def index():
    """
    Home page with greeting and a form for the user to enter a place name
    """
    return render_template("index.html", username="Friend")


@app.route("/nearest_mbta", methods=["POST"])
def nearest_mbta():
    """
    return the nearest MBTA station with the temperature of that place
    """
    place_name = request.form.get("place_name")  # get the place name from the form filled out by user
    if place_name:
        if "Boston" not in place_name:
            formatted_place_name = "Boston " + place_name
        else:
            formatted_place_name = place_name # struggled to understand why place_name was no longer printing correctly so used chatgpt to debug 
        
        station, accessible = mbta_helper.find_stop_near(place_name)
        latitude, longitude = mbta_helper.get_lat_lng(place_name)
        if station and latitude and longitude:
            weather = mbta_helper.get_weather(latitude, longitude)
            return render_template("mbta.html", station=station, accessible=accessible, weather=weather, place_name=formatted_place_name)
        else:
            return render_template("error.html")


if __name__ == "__main__":
    app.run(debug=True)
