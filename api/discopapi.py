import json
import random
import requests
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select
from algorithm import ArtistScraper
from spot import spot

#####################################################
## ## ## ## Initial Setup ## ## ## ## ## ## ## ## ###

## Setup FastAPI ##
discopapi = FastAPI()

origins = [
    "*",
]

discopapi.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

## Setup Database ##
class Artist(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    spot_id: str
    name: str = Field(index=True)
    monthly_listeners: int
    date_added: str
    tags: str | None = None

sqlite_filename = "database.db"
sqlite_url = f"sqlite:///{sqlite_filename}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_test_artists():
    artist_1 = Artist(spot_id='3TVXtAsR1Inumwj472S9r4', name="Drake", monthly_listeners=123456789, date_added="5/15/24, 14:39:21")
    artist_2 = Artist(spot_id='7tYKF4w9nC0nq9CsPZTHyP', name="SZA", monthly_listeners=567899, date_added="5/15/24, 14:45:46")
    artist_3 = Artist(spot_id='5IXHcQG5Sw0xYlRWuWEkL9', name="stoic da poet", monthly_listeners=12, date_added="5/15/24, 15:03:01")

    with Session(engine) as session:
        session.add(artist_1)
        session.add(artist_2)
        session.add(artist_3)

        session.commit()


def main():
    create_db_and_tables()
    create_test_artists()

# if __name__ == "__main__":
#     main()

## Define Classes ##
class ArtistURI(BaseModel):
    uri: str

class ArtistID(BaseModel):
    id: float


#####################################################
## ## ## ## API Endpoints ## ## ## ## ## ## ## ## ###

@discopapi.get("/")
def read_root():
    return {"Root Request": 200}

@discopapi.get("/test")
def test():
    main()
    return {"Test Request": 200, "Info": "testing"}

@discopapi.get("/grab/{uri}")
def grab_listeners(uri: Optional[str] = None):
    urilisteners = ArtistScraper("https://open.spotify.com/artist/" + uri)
    urilisteners.get_html()
    return urilisteners.get_monthlyListeners()

# @discopapi.get("/discopapi/view")
# def view_all():
#     data = view()
#     return {'artists': data}

@discopapi.get("/discopapi/view")
def view_all():
    data = view()
    return {'artists': data}
    
# @discopapi.post("/discopapi/save")
# def save(artist: ArtistURI):
#     print(artist.uri)
#     save_artist(artist.uri)
#     data = view()
#     return {'artists': data}

@discopapi.post("/discopapi/save")
def save_db(artist: ArtistURI):
    print(artist.uri)
    saved = save_artist(artist.uri)
    if not saved:
        raise HTTPException(status_code=500, detail="Artist Already Exists")
    data = view()
    return {'artists': data}

# @discopapi.get("/discopapi/savetst")
# def save_db_tst():
#     test_uri = 'https://open.spotify.com/artist/1URnnhqYAYcrqrcwql10ft'   # 21 sav
#     # test_uri = 'https://open.spotify.com/artist/3TVXtAsR1Inumwj472S9r4'     # Drake
#     save_artist_db(test_uri)
#     data = viewdb()
#     return {'artists': data}

@discopapi.post("/discopapi/delete")
def delete(artist_id: ArtistID):
    dr = delete_artist(artist_id.id)
    if dr is True:
        data = view()
        return {'artists': data}
    else:
        return {'artists': None}


#####################################################
## ## ## ## Key Functions ## ## ## ## ## ## ## ## ###

# DEPRECATED Return all data for viewing
# def view():
#     db = {}
#     with open('artists.json') as f:
#         db = json.load(f)
#     return {'artists': db}

# View all objects in database using SQLModel
def view():
    saved_artists = []
    with Session(engine) as session:
        statement = select(Artist)
        results = session.exec(statement)
        for artist in results:
            saved_artists.append(artist)

    return {'artists': saved_artists}

###
# DEPRECATED 
#   Saves the specified artist to the database
#   'artist' param must be a Spotify URI
###
# def save_artist(url: str):
#     error = None

#     # 0. Get URI and find Artist data (name & follower count)
#     uri = str(url).split('/')[4]
#     artist_data = spot(uri)
    
#     # 1. Open JSON file
#     db = {}
#     with open('artists.json') as f:
#         db = json.load(f)

#     # 2. Read JSON file & get artist list
#     artists = db['artists']

#     # 3. Check if artist exists. Return if it does
#     for a in artists:
#         if a['name'] == artist_data['name']:
#             print('Artist Already Exists')
#             return False
      
#     # 4. If not, proceed to create artist object (id, count, timestamp)
#     count = get_count(uri)
#     date_added = datetime.now().replace(microsecond=0).strftime("%m/%d/%Y, %H:%M:%S")
#     new_artist = {
#         'id': round(random.random()*1000000,7),
#         'name': artist_data['name'],
#         'count': count,
#         'followers': artist_data['followers'],
#         'date': date_added,
#         'tags': []
#     }

#     # 5. Add artist obj to JSON
#     artists.append(new_artist)
#     db['artists'] = artists
#     updated_db = json.dumps(db, indent=4)
    
#     # 6. Write to JSON file
#     with open('artists.json', 'w') as f:
#         f.write(updated_db)
#     return True

def save_artist(url: str):
    error = None

    # 0. Get URI and find Artist data (name & follower count)
    uri = str(url).split('/')[4]
    artist_data = spot(uri)
    print(artist_data)
    if artist_data is False:
        error = "Failed to fetch artist name"
        return error
    
    # 1. Begin SQLModel db Session
    with Session(engine) as session:
        # Try to get .one() using the spotify_id:
        #   If it returns an error, we know there is nothing there & we can add the artist
        #   If it returns an object, we know it exists & we shouldn't add this artist
        try:
            existing_artist = session.exec(select(Artist).where(Artist.spot_id == artist_data['spotify_id'])).one()
            print("Artist Found: ", existing_artist)
            return False
        except:
            print("Could not find the object in the database... adding new artist")
      
        # Create Artist object
        count = get_count(uri)
        added_date = str(datetime.now().replace(microsecond=0).strftime("%m/%d/%Y, %H:%M:%S"))
        new_artist = Artist(spot_id=artist_data['spotify_id'], name=artist_data['name'], monthly_listeners=count, date_added=added_date)

        session.add(new_artist)

        session.commit()

        print("New Artist", new_artist.spot_id, new_artist.name)

    return True



# Delete a single artist by id
def delete_artist(id: float):
    db = {}
    with open('artists.json') as f:
        db = json.load(f)

    found = find_artist_by_id(db, id)
    if not found:
        return False
    db['artists'][:] = [d for d in db['artists'] if d.get('id') != id]
    updated_db = json.dumps(db)
    return save_db(updated_db)

#####################################################
## ## ## ## Auxilliary Functions ## ## ## ## ## ## ##

# Return artist object if found in Db, otherwise return False
def find_artist_by_id(db, id):
    for a in db['artists']:
        if a['id'] == id:
            return a
    return False

# Pass in JSON database and write to file
def save_db(updated_db):
    with open('artists.json', 'w') as f:
        f.write(updated_db)
    return True

### 
# Function to retrieve count from Spotify API
# Takes in a Spotify URI
def get_count(artist_uri: str):
    # artist_uri = '3TVXtAsR1Inumwj472S9r4'
    # print('getting uri: ', artist_uri)
    request_url = f'http://127.0.0.1:8000/grab/{artist_uri}'
    r = requests.get(request_url)
    if r.status_code == 200:
        return int(r.text)
    else:
        return False