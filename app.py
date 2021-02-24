#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import datetime
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for,abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app,session_options={"expire_on_commit": False})
migrate = Migrate(app,db)

# Completed: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    # Define the table name
    __tablename__ = 'venue'
    # Define all the attributes of the table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    shows = db.relationship('Show',backref='venues',lazy=True) #Defining the Relationship
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(400))
    # Implement the repr method for object representation
    def __repr__(self):
      return f'<Venue id:{self.id} name:{self.name} city:{self.city}>'


    # Completed: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    #Define the name of the table
    __tablename__ = 'artist'
    #Define all the attributes of the table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    shows = db.relationship('Show',backref='artists',lazy=True) #Defining the relationship
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(400))
    # Implement the repr method for object representation
    def __repr__(self):
      return f'<Artist id:{self.id} name:{self.name}>'

    # Completed: implement any missing fields, as a database migration using Flask-Migrate

# Completed Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  #Define the name of the table
  __tablename__ = 'shows'
  #Define all the attributes of the table
  id = db.Column(db.Integer,primary_key=True,autoincrement=True)
  artist_id = db.Column(db.Integer,db.ForeignKey('artist.id'),primary_key=True,nullable=False)
  venue_id = db.Column(db.Integer,db.ForeignKey('venue.id'),primary_key=True,nullable=False)
  start_time = db.Column(db.DateTime,nullable=False)
  #Implement the repr method for object representation
  def __repr__(self):
    return f'<Show id:{self.id} artist_id:{self.artist_id} venue_id:{self.venue_id}>'
  

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime


#----------------------------------------------------------------------------#
# Helper Methods.
#----------------------------------------------------------------------------#

def create_new_artist():
  '''A Helper Method to Create a Artist
  Returns a New Artist Object.'''
  #Name of the Artist
  artist_name = request.form['name']
  #City Where Artist Lives
  artist_city = request.form['city']
  #State Where City is located 
  artist_state = request.form['state']
  #Phone Number of the artist
  artist_phone = request.form['phone']
  #List of Artist genres
  artist_genres = request.form.getlist('genres')#Using getlist method because an artist can have multiple genres
  #Link to the Artist Image
  artist_image_link = request.form['image_link']
  #Link to the Artist Facebook Page
  artist_facebook_link = request.form['facebook_link']
  #Link to the Artists Personal Website
  artist_website = request.form['website']
  #If Artist seeks venue then artist_seeking_venue = true else artist_seeking_venue = false
  if 'seeking_venue' in request.form:
     artist_seeking_venue = True
  else:
     artist_seeking_venue = False
  #Artist seeking description
  artist_seeking_description = request.form['seeking_description']
  #Create an instance of Artist
  new_artist = Artist(name=artist_name,city=artist_city,state=artist_state,phone=artist_phone,genres=artist_genres,image_link=artist_image_link,facebook_link=artist_facebook_link,website=artist_website,seeking_venue=artist_seeking_venue,seeking_description=artist_seeking_description)
  #Return the New Artist Instance Created
  return new_artist

def create_new_venue():
  '''A Helper Method to Create a Venue
  Returns a New Venue Object. '''
  #Name of the Venue
  venue_name = request.form['name']
  #City Where Venue is Located
  venue_city = request.form['city']
  #State Where City is Located
  venue_state = request.form['state']
  #Contact Number of the Venue
  venue_phone = request.form['phone']
  #List of genres required by the venue
  venue_genres = request.form.getlist('genres')#Using getlist method because a venue can have multiple genres listed
  #Complete Address of the Venue
  venue_address = request.form['address']
  #Link to the Image of the Venue
  venue_image_link = request.form['image_link']
  #Link to the Facebook Page of the Venue
  venue_facebook_link = request.form['facebook_link']
  #Link to the Website of the Venue
  venue_website = request.form['website']
  #If venues seek authors then venue_seeking_talent=true else venue_seeking_talent = false
  if 'seeking_talent' in request.form:
    venue_seeking_talent = True
  else:
    venue_seeking_talent = False
  #Seeeking Description as specified by the venue
  venue_seeking_description = request.form['seeking_description']
  #Create an Instance of Venue
  new_venue = Venue(name=venue_name,city=venue_city,state=venue_state,phone=venue_phone,genres=venue_genres,address=venue_address,image_link=venue_image_link,facebook_link=venue_facebook_link,website=venue_website,seeking_talent=venue_seeking_talent,seeking_description=venue_seeking_description)
  #Return the New Venue Instance Created
  return new_venue

def create_new_show():
  '''A Helper Method to Create a Show
  Returns a New Show Object.'''
  #Id of the Artist
  artist_id = request.form['artist_id']
  #Id of the Venue
  venue_id = request.form['venue_id']
  #Start time of the show
  show_start_time = request.form['start_time']
  #Create an instance of show
  new_show = Show(artist_id=artist_id,venue_id=venue_id,start_time=show_start_time)
  #Return the New Show Instance Created
  return new_show


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

#Home Route
@app.route('/')
def index():
  #Renders the Home Page Template for the Fyyur Web Application
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  #This method returns venues which are grouped by cities and then grouped by state
  #Get all the info about all the places
  places = Venue.query.with_entities(Venue.city,Venue.state,func.count(Venue.id)).group_by(Venue.city,Venue.state).all()
  #List to store information for every venue
  venue_info = []
  #Iterate through all the places
  for place in places:
    #Get all the venues in the place
    venues = Venue.query.filter_by(state=place.state).filter_by(city=place.city).all()
    data_venue = []
    #Now Again iterate through all the venues in a place
    for venue in venues:
      num_upcoming_shows = len(Show.query.filter(Show.venue_id==venue.id).filter(Show.start_time>datetime.now()).all())
      data_venue.append({
        "id":venue.id,#Id of the venue
        "name":venue.name,#Name of the venue
        "num_upcoming_shows":num_upcoming_shows#Number of Upcoming shows at this venue
      })
    #Now append all the venue info collected
    venue_info.append({
      "city":place.city,#Name of the city where the venue is located
      "state":place.state,#Name of the state where the venue is located
      "venues":data_venue#List of the venues
    })
  #Return the template along with the data
  return render_template('pages/venues.html', areas=venue_info)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  #This method searches for all the venues which includes the search_term as a substring in the name of the venue
  #First fetch the search_term from the request body
  venue_name = request.form['search_term']
  #This method is case insensitive so use the ilike method while querying the database
  venues_set = Venue.query.filter(Venue.name.ilike('%'+venue_name+'%')).all()
  #List to store the information about venues
  venues = []
  #Iterate through all the venues
  for venue in venues_set:
    #Append the venue info
    num_upcoming_shows = len(Show.query.filter(Show.venue_id == venue.id).filter(Show.start_time>datetime.now()).all())
    venues.append({
        "id":venue.id,#Id of the venue
        "name":venue.name,#Name of the venue
        "num_upcoming_shows":num_upcoming_shows#Number of upcoming shows at this venue
    })
  #Count the number of venues found with the given search_term
  no_of_venues = len(venues)
  #Store the final response
  venues_found={
    "data":venues,
    "count":no_of_venues
  }
  #Return the template along with the data
  return render_template('pages/search_venues.html', results=venues_found, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  #First Check if there is a venue with the given id
  venue = Venue.query.get(venue_id)
  #If there is no venue with the given id then abort thr request and show a 404 error page.
  if venue is None:
    return render_template('errors/404.html')
  #Create dictionary storing the details of the venue
  venue_details = {
    "id":venue.id,
    "name":venue.name,
    "genres":venue.genres,
    "address":venue.address,
    "city":venue.city,
    "state":venue.state,
    "phone":venue.phone,
    "website":venue.website,
    "facebook_link":venue.facebook_link,
    "seeking_talent":venue.seeking_talent,
    "seeking_description":venue.seeking_description,
    "image_link":venue.image_link
  }
  #Find the list of the previous shows held at the venue
  previous_shows = Show.query.filter(Show.venue_id == venue_id).filter(Show.start_time < datetime.now()).all()
  #Find the list of the future shows which are going to be held at this venue
  future_shows = Show.query.filter(Show.venue_id == venue_id).filter(Show.start_time > datetime.now()).all()
  #List for storing the details of past shows
  past_shows_info= []
  #Iterate through every show in the previous shows
  for show in previous_shows:
    #Find the details of the artist who played at this venue
    artist_details = Artist.query.get(show.artist_id)
    #Append the details of the previous show to the list
    past_shows_info.append({
      "artist_id":show.artist_id,#Id of the artist
      "artist_name":artist_details.name,#Name of the artist
      "artist_image_link":artist_details.image_link,#Link to the artist image
      "start_time":show.start_time.strftime("%Y-%m-%d %H:%M:%S")#Show time in (YY-MM-DD) format
    })
  #List for storing the details of future shows
  upcoming_shows_info = []
  #Iterate through every show in the future shows
  for show in future_shows:
    #Find tehe details of the artist who will play at this venue
    artist_details = Artist.query.get(show.artist_id)
    #Append the details of the future show to the list
    upcoming_shows_info.append({
      "artist_id":show.artist_id,#Id of the artist
      "artist_name":artist_details.name,#Name of the artist
      "artist_image_link":artist_details.image_link,#Link to the artist image
      "start_time":show.start_time.strftime("%Y-%m-%d %H:%M:%S")#Show time in (YY-MM-DD) format
    })
  #Store the information about past_shows in the response
  venue_details["past_shows"] = past_shows_info
  #Store the information about future shows in the response
  venue_details["upcoming_shows"] = upcoming_shows_info
  #Count the number of past shows held at this venue
  venue_details["past_shows_count"] = len(past_shows_info)
  #Count the number of future shows held at this venue
  venue_details["upcoming_shows_count"] = len(upcoming_shows_info)
  #Return the response and redirect the user
  return render_template('pages/show_venue.html', venue=venue_details)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  #Renders the Venue Form
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
  try:
    #Create a New Venue
    venue = create_new_venue()
    #Add the Venue to the the database
    db.session.add(venue)
    #Persist the changes to the database
    db.session.commit()
  except:
    error = True
    #If there is any error then rollback to previous commit
    db.session.rollback()
    #Print the logs for debugging
    print(sys.exc_info())
  finally:
    #Finally Close the Session
    db.session.close()
  #If there is no error then flash a success message
  if not error:
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  #If there is an error then flash a error message
  else:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  #This method deletes the venue from the database
  error = False
  try:
    #Fetch the venue 
    venue = Venue.query.get(venue_id)
    #Delete the venue by using delete method
    db.session.delete(venue)
    #Persist the change in the database
    db.session.commit()
  #If there any errors then except block will be executed
  except:
    error = True
    #Print the logs for debugging
    print(sys.exc_info())
    #Rollback changes if any errors ocuur
    db.session.rollback()
  finally:
    #Finally close the session
    db.session.close()
  if error:
    flash(f'Error Venue {venue_id} could not be deleted')
  else:
    flash(f'Venue {venue_id} was deleted successfully')
   #Return the template along with the data
  return render_template('pages/venues.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  #This method returns the list of all the artist
  artists_info = Artist.query.all()
  #Return the template along with the data
  return render_template('pages/artists.html', artists=artists_info)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  #This method searches for all the venues which includes the search_term as a substring in the name of the venue
  #First fetch the search_term from the request body
  artist_name = request.form['search_term']
  #This method is case insensitive so use ilike while executing the query
  artists = Artist.query.filter(Artist.name.ilike('%'+artist_name+'%')).all()
  #List for storing the information about the artists
  artist_info = []
  #Iterate through all the artists
  for artist in artists:
    #Append the required information to the list
    num_upcoming_shows = len(Show.query.filter(Show.artist_id == artist.id).filter(Show.start_time > datetime.now()).all())
    artist_info.append({
      "id":artist.id,
      "name":artist.name,
      "num_upcoming_shows":num_upcoming_shows
    })
  #Count the number of artists found with the given search term
  no_of_artists = len(artist_info)
  #Store the final response
  artists_found={
    "data":artist_info,
    "count":no_of_artists
  }
  #Return the template along with the data
  return render_template('pages/search_artists.html', results=artists_found, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  #Shows the venue page with the given venue_id
  #First Check if there is any artist with the given id
  artist = Artist.query.get(artist_id)
  #If there is no artist with the given id then abort thr request and show 404 error page
  if artist is None:
    return render_template('errors/404.html')
  #Create a dictionary to store the details of the artist
  artist_details = {
    "id":artist.id,
    "name":artist.name,
    "genres":artist.genres,
    "city":artist.city,
    "state":artist.state,
    "phone":artist.phone,
    "website":artist.website,
    "facebook_link":artist.facebook_link,
    "seeking_venue":artist.seeking_venue,
    "seeking_description":artist.seeking_description,
    "image_link":artist.image_link
  }
  #Find the details of the past shows attended by the artist
  previous_shows = Show.query.filter(Show.artist_id == artist_id).filter(Show.start_time < datetime.now()).all()
  #Find the details of the future shows 
  future_shows = Show.query.filter(Show.artist_id == artist_id).filter(Show.start_time > datetime.now()).all()
  #List to store the details of the previous shows
  past_shows_info = []
  #Iterate through every show in previous shows
  for show in previous_shows:
    #Find the details of the venue where the artist performed previously
    venue_details = Venue.query.get(show.venue_id)
    #Append the required information to the list
    past_shows_info.append({
      "venue_id":show.venue_id,#Id of the Venue
      "venue_name":venue_details.name,#Name of the Venue
      "venue_image_link":venue_details.image_link,#Image Link of the Venue
      "start_time":show.start_time.strftime("%Y-%m-%d %H:%M:%S"),#Show start time in (YY-MM-DD) format
    })
  #List to store the details of the future shows
  upcoming_shows_info = []
  #Iterate through every show in future shows
  for show in future_shows:
    #Find the details of the venue where the artist is going o perform
    venue_details = Venue.query.get(show.venue_id)
    upcoming_shows_info.append({
      "venue_id":show.venue_id,#Id of the Venue
      "venue_name":venue_details.name,#Name of the Venue
      "venue_image_link":venue_details.image_link,#Image Link of the Venue
      "start_time":show.start_time.strftime("%Y-%m-%d %H:%M:%S"),#Show start time in (YY-MM-DD) format
    })
  #Store the details of the past shows
  artist_details["past_shows"] = past_shows_info
  #Store the details of the future shows
  artist_details["upcoming_shows"] = upcoming_shows_info
  #Count the number of shows played by the artist in the past
  artist_details["past_shows_count"] = len(past_shows_info)
  #Count the number of shows booked by the artist
  artist_details["upcoming_shows_count"] = len(upcoming_shows_info)
  #Return the response and redirect the user
  return render_template('pages/show_artist.html', artist=artist_details)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  if artist is None:
    return render_template('errors/404.html')
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  error = False
  artist = Artist.query.get(artist_id)
  #If there is no artist with the given artist_id then abort thr request
  if artist == None:
    abort(404)
  #If there is an artist with the given artist_id then update the details of the artist
  try:
    if "name" in request.form:
      artist.name = request.form['name']
    if "city" in request.form:
      artist.city = request.form['city']
    if "state" in request.form:
      artist.state = request.form['state']
    if "phone" in request.form:
      artist.phone = request.form['phone']
    if "genres" in request.form:
      artist.genres = request.form.getlist('genres')#Using a list because there can be multiple genres
    if "image_link" in request.form:
      artist.image_link = request.form['image_link']
    if "facebook_link" in request.form:
      artist.facebook_link = request.form['facebook_link']
    if "website" in request.form:
      artist.website = request.form['website']
    if "seeking_venue" in request.form:
      artist.seeking_venue = True 
    else:
      artist.seeking_venue = False
    if "seeking_description" in request.form:
      artist.seeking_description = request.form['seeking_description']
    #Finally persis the changes to the database
    db.session.commit()
  except:
    error = True
    #If there is any during updation then roll back
    db.session.rollback()
    #Print the logs for debugging
    print(sys.exc_info())
  finally:
    #Close the session 
    db.session.close()
  #If there is any error then flash a error message
  if error:
    flash(f'Error Artist details {artist.name} could not be updated')
  #If the update is successfull then flash a success message
  else:
    flash(f'Artist {artist.name} details updated successfully')
  #ARedirect the user to the artist page
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  if venue is None:
    return render_template('errors/404.html')
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  error = False
  venue = Venue.query.get(venue_id)
  #First Check if there is any venue with the given venue_id
  #If there is no venue with the given venue_id then abort the request
  if(venue == None):
    abort(404)
  #If there is a venue with the given venue_id then perform the update
  try:
    if "name" in request.form:
      venue.name = request.form['name']
    if "city" in request.form:
      venue.city = request.form['city']
    if "state" in request.form:
      venue.state = request.form['state']
    if "phone" in request.form:
      venue.phone = request.form['phone']
    if "genres" in request.form:
      venue.genres = request.form.getlist('genres')#Using list because there can be multiple genres
    if "address" in request.form:
      venue.address = request.form['address']
    if "image_link" in request.form:
      venue.image_link = request.form['image_link']
    if "facebook_link" in request.form:
      venue.facebook_link = request.form['facebook_link']
    if "website" in request.form:
      venue.website = request.form['website']
    if "seeking_talent" in request.form:
      venue.seeking_talent = True 
    else:
      venue.seeking_talent = False
    if "seeking_description" in request.form:
      venue.seeking_description = request.form['seeking_description']
    #Persist the changes to the database
    db.session.commmit()
  except:
    error = True
    #If there is any error then rollback to previous commit
    db.session.rollback()
    #Print the logs for debugging
    print(sys.exc_info())
  finally:
    #Finally close the session
    db.session.close()
  #If any error occured then flash a error message
  if error:
    flash(f'Error Venue {venue.name} details could not be updated')
  #If the updation is successfull then flash a success message
  else:
    flash(f'Venue {venue.name} details updated successfully')
  #Redirect the user to the venue page
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  #Renders a Artist Form
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  error = False
  try:
    artist = create_new_artist()
    db.session.add(artist)
    #Persist the changes to the database
    db.session.commit()
  except:
    error = True
    #If there is any error then rollback to previous commit
    db.session.rollback()
    #Print the logs for debugging
    print(sys.exc_info())
  finally:
    #Finally close the session
    db.session.close()
  #If there is no error then flash an success message
  if not error:
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # on successful db insert, flash success
  #If there is an error then flash an error message
  else:
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  #Render the home page template
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # Perform a Join Query to get the info about all the shows
  shows_list = Show.query.join(Venue).join(Artist).all()
  #List for showing information about every show
  shows_info = []
  #Iterate through every show
  for show in shows_list:
    #Add the required fields for each show to the list
    shows_info.append({
      "venue_id":show.venue_id,#Id of the Venue Where Show was held
      "venue_name":show.venues.name,#Name of the venue where show was held
      "artist_id":show.artist_id,#Id of the Artist Who Played at this show 
      "artist_name":show.artists.name,#Name of the Artist Who Played at this Show
      "artist_image_link":show.artists.image_link,#Link to the image of artist
      "start_time":show.start_time.strftime('%Y-%m-%d %H:%M:%S')#Show time in (YY-MM-DD) format
    })
  #Render the template along with the data
  return render_template('pages/shows.html', shows=shows_info)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  #Renders a Show Form 
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  error = False
  try:
    #Fetch all the details from the request body
    artist_id = request.form['artist_id']
    venue_id = request.form['venue_id']
    start_time = request.form['start_time']
    #Create an Object of Show
    new_show = Show(artist_id=artist_id,venue_id=venue_id,start_time=start_time)
    #Add it to the database
    db.session.add(new_show)
    #Commit so that changes persist in the database
    db.session.commit()
  #If any errors occur then except block will be executed
  except:
    error = True
    #Rollback if any errors occur
    db.session.rollback()
    #Print the logs for debugging
    print(sys.exc_info())
  finally:
    #At last close the session
    db.session.close()
  if not error:
    # on successful db insert, flash success
    flash('Show was successfully listed!')
  else:
    flash('An error occurred. Show could not be listed.')
  # Completed: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
   #Return the template along with the data
  return render_template('pages/home.html')


# Error Handlers for HTTP Status Code 404(Resource Not Found)
@app.errorhandler(404)
def not_found_error(error):
  # Render the error 404 template
  return render_template('errors/404.html'), 404
  
# Error Handlers for HTTP Status Code 500(Bad Request)
@app.errorhandler(500)
def server_error(error):
  #Render the error 500 template
  return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
'''
