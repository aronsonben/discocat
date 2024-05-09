# ANRdiscocatPOC

The ever-elusive AnR Discocat idea that I've never quite implemented. Somehow completed most of the backend in a single day sometime around March 2024. This directory adds a Vite-based React.js front-end.

## Development

**The current implementation requires *three(!!!) servers!*** You must run the Flask app from `app.py` *and* the [Spotify-Monthly-Listeners-API](https://github.com/toluooshy/Spotify-Monthly-Listeners-API) from `Spotify-Monthly-Listeners-API/main.py`, each running on ports 5000 and 8000s respectively. Newly added in late April 2024, you must now also run `npm run dev` to start the frontend of the Vite app.

My next task is looking to merge these before I dive much deeper in development.

Also, don't forget to **add the environment variables in `.env` to your dev environment!**

### How to Start

(From the `/api` directory) 
In one terminal, run:

`. .venv/Scripts/activate`
`flask --app api run --debug`

(From the `/api/Spotify-Monthly-Listeners-API` directory) 
In another, run:

`. .venv/Scripts/activate`
`uvicorn main:spapi --reload`

(From the top-level `discocatfe` directory) 
In yet another, run: 

`npm run dev`

### Deployment Notes
*For keeping track of how deployment process is being implemented.*

Following this tutorial: https://blog.miguelgrinberg.com/post/how-to-deploy-a-react--flask-project


### Development Notes & Milestones

#### v0.0.1
*Simple and basic version*
- [x] Add new artist from Spotify URI
- [x] Display list of artists upon load
- [x] Add new artist to list
- [x] Delete specified artist

#### v0.0.2
- [x] Update artist list immediately after save/delete
- [x] Basic improvements to base UI (user input & artist list)
- [x] Display monthly listeners & date in better format
- [x] Remove delete btn from header

#### v0.0.3
- [x] Use more official framework, library, or db for displaying artists with pagination --> ***going with [PrimeReact](https://primereact.org/installation/)***
- [x] Improve overall UI to a clean-ish basis
*completed 5.8.24*

#### v0.0.3_Hotfix
- [x] Combined my `api` with Spotify-Monthly-Listener-API's `spapi` to exist as a single backend api service using FastAPI instead of Flask

#### v0.0.4
- [] Enable responsive UI (so mobile AND web look clean)
- [] Enable deployment processes (how does uvicorn work in production?)

#### *Future*
- [ ] Update monthly listeners and show change
- [ ] Track changes to monthly listeners over time (v1: via logs)
- [ ] Display *tags*
- [ ] Edit an artist after adding
- [ ] Spotify API integration to link to artist pages & artist search

#### *'Someday' Ideas*
- User accounts
- Add charts for tracking changes over time, instead of logs
- Awards for having artists with big jumps
- "Seasons" like in BBGM, where only artists added in X timeframe are counted and people are rewarded for best finds
- Trending list of artists being saved

#### 💭 Development Ponderings

##### Minimum Viable Product (MVP)
**Summary:** A&R DiscoCat (to be renamed) is a tool that enables fans of music discovery to bookmark their findings and watch their favorite new artists rise to the top. Artists can be saved and their key performance indicators (namely, Monthly Listeners and Followers via Spotify) tracked over time. A&R Discocat solves the "hipster problem" in music so there are no more fedoras saying they "knew so & so way before anyone else". With Discocat, simply Stamp* your Discoveries* when you find them.

**term ideas for later?*

**MVP?** Discocat would be considered a product that I think people would find value in if you could reliably save artists you discover and keep an eye on monthly listener changes over time. 

🤔Think of leverson discovering a new artist with 3,000 monthly listeners. He saves that artist. Why would he come back here? Only to see if his first slew of saved artists are now at 30,000 or 300,000 listeners. He should get some kind of award for that.

##### Tags
Before implementing tags, I feel like I ought to pick a better ~~storage~~ *display* format for artists. 
A manual list is not the move because I think `tags` should be assigned/edited after an artist is added.
May 1, 2024: looking for solutions for displaying editable tables in React.js (again...)
Keep in mind that tags should have their own "db table" and those should be displayed as options when adding tags to artists.
🤔After thinking about the MVP, I think tags are actually less important than I first thought. They are helpful when time passes but for now, just saving & tracking the monthly listeners is what really matters.

##### Design

[Neubrutalism](https://ux.stackexchange.com/questions/145559/what-is-the-design-system-of-gumroad)
[Brutalism](https://webdesign.tutsplus.com/its-tough-out-there-a-look-at-brutalism-in-web-design--cms-26545a)