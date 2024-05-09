import { useState, useEffect, useRef } from 'react'
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Paginator } from 'primereact/paginator';
import Navbar from './components/Navbar';
import './App.css'

// function ArtistListOld() {
//   const [currentArtists, setCurrentArtists] = useState([]);

//   return (
//     <div>
//           <div className="artistList">
//             <div className="artistRows">
//               <div className="artistListHeaders ArtistCard">
//                 <p id="artistname">Artist Name</p>
//                 <p id="artistcount">Monthly Listeners</p>
//                 <p id="artistdate">Date Added</p>
//               </div>
//               <button type="button" disabled={true} className="artistDel disabled">Filter</button>
//             </div>
//             {currentArtists.map(artist => (
//               <div className="artistRows" key={artist.id+artist.name}>
//                 <ArtistCard artist={artist}/>
//                 <button className="artistDel" onClick={() => deleteCall(artist.id)}>Delete</button>
//               </div>
//             ))}
//           </div>
//         </div>
//   );
// }

function InstructionBar() {
  const divRef = useRef(null);
  const [instructionsOpen, setInstructionsOpen] = useState(true);

  return (
    <div>
      <fieldset className="InstructionAccordion">
        <legend>
          <span id="legendLeft">Instructions</span>
          <button id="legendOpenClose" onClick={() => setInstructionsOpen(!instructionsOpen)}>
            {!instructionsOpen ? '+' : '-'}
          </button>
        </legend>
        <div 
          className="InstructionList" 
          onClick={() => setInstructionsOpen(!instructionsOpen)} 
          style={{ opacity: instructionsOpen ? 1 : 0, height: instructionsOpen ? '125px' : 0 }}
          ref={divRef}
        >
          {divRef ? 
            (!instructionsOpen && (divRef.current.style.opacty == 0) ? <p>HI</p> : 
              <>
                <p>1. Enter your newly discovered artist URI into input below.</p>
                <p>2. Saved artists will be displayed in the Artist List beneath.</p>
                <p>3. Come back later to see how the count for your artists is doing.</p>
              </>
            ) :
            <p>WHY</p>
          }
          
        </div>
      </fieldset>
    </div>
  );
}

function DiscoveryInput({inputValue, setInputValue, save}) {
  return (
    <div className="card discoveryInput">
      <div className="discoveryInputLabel">
        <div>
          <label>Enter an Artist's Spotify URI:</label>
          <p id="inputex">i.e. https://open.spotify.com/artist/3TVXtAsR1Inumwj472S9r4</p>
        </div>
      </div>
      <input 
        className="discoveryInputBox"
        type="text" 
        placeholder="Spotify URI" 
        value={inputValue} 
        onChange={(e) => setInputValue(e.target.value)}></input>
      <button type="button" onClick={() => save()}>save</button>
    </div>
  );
}

function ArtistList({currentArtists, first, onPageChange}) {
  const deleteBodyTemplate = (artist) => {
    return <button className="artistDel" onClick={() => deleteCall(artist.id)}>Delete</button>
  }

  const dateBodyTemplate = (artist) => {
    return <ArtistCard artist={artist} parameter={"date"} />
  }

  const countBodyTemplate = (artist) => {
    return <ArtistCard artist={artist} parameter={"count"} />
  }

  const paginatorLeft = <button type="button" className="paginatorBtn" text> {'<'} </button>;
  const paginatorRight = <button type="button" className="paginatorBtn" text> {'>'} </button>;
  
  const paginatorTemplate = {
    layout: "PrevPageLink CurrentPageReport NextPageLink",
    PrevPageLink: (options) => {
      return (
        <button onClick={options.onClick} className="paginatorBtn" text> {'<'} </button>
      );
    },
    NextPageLink: (options) => {
      return (
        <button onClick={options.onClick} className="paginatorBtn" text> {'>'} </button>
      );
    }
  }

  return (
    <DataTable value={currentArtists} paginator rows={5} style={{ justifyContent: 'center', fontSize: '14px' }}
      paginatorTemplate={paginatorTemplate} first={first} onPageChange={onPageChange}>
      <Column field="name" header="Artist Name" style={{ width: '25%', textAlign: 'left' }}></Column>
      <Column field="count" header="Monthly Listeners" body={countBodyTemplate} style={{ width: '25%', textAlign: 'left' }}></Column>
      <Column field="date" header="Date Added" body={dateBodyTemplate} style={{ width: '20%', textAlign: 'left' }}></Column>
      <Column field="delete" header="Delete" body={deleteBodyTemplate} style={{ width: '10%', textAlign: 'right' }}></Column>
    </DataTable>
  );
}

function ArtistCard({artist, parameter}) { 

  const commas = (count) => {
    let strcount = String(count);
    let nucount = '';
    let lngct = 0;

    // base case: three-digit number or less
    if(strcount.length-1 < 3) {
      return count;
    }
    
    // add commas
    for(let i = strcount.length-1; i >= 0 ; i--) {
      lngct = ++lngct;
      let ch = strcount.charAt(i);
      nucount = nucount.concat(strcount.charAt(i))
      if(i > 0 && lngct % 3 == 0) {
        nucount = nucount.concat(',');
      }
    }
    
    // reverse & return
    return nucount.split("").reverse().join("");
  }

  const dateformatter = (date) => {
    return date.split(",")[0];
  }

  if (parameter == "date") {
    return (
      <p id="artistdate">{dateformatter(artist.date)}</p>
    )
  } else if (parameter == "count") {
    return (
      <p id="artistcount">{commas(artist.count)}</p>
    )
  } else {
    return (
      <div className="ArtistCard">
        <p id="artistname">{artist.name}</p>
        <p id="artistcount">{commas(artist.count)}</p>
        <p id="artistdate">{dateformatter(artist.date)}</p>
      </div>
    )
  }
}

function App() {
  const [currentArtists, setCurrentArtists] = useState([]);
  const [discoveryInput, setDiscoveryInput] = useState('https://open.spotify.com/artist/3TVXtAsR1Inumwj472S9r4');
  const [first, setFirst] = useState(0);

  useEffect(() => {
    fetch('/discopapi/view').then(res => res.json()).then(data => {
      console.log(data);
      setCurrentArtists(data.artists.artists.artists);
    });
  }, []);

  const saveCall = async () => {
    console.log(discoveryInput)
    fetch('/discopapi/save', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        uri: discoveryInput,
      }),
    })
    .then(res => res.json())
    .then(data => {
      console.log(data);
      setCurrentArtists(data.artists.artists.artists);
    });
    return (
      <p>hi</p>
    );
  }

  const deleteCall = async (artistId) => {
    console.log('delete..', artistId);
    fetch('/discopapi/delete', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        id: artistId,
      }),
    })
    .then(res => res.json())
    .then(data => {
      console.log(data);
      setCurrentArtists(data.artists.artists.artists);
    });
    return null;
  }

  const onPageChange = (event) => {
    setFirst(event.first);
  };

  return (
    <>
      <Navbar />
      <div id="app">
        <div className="AppHeader">
          <h2 className="TempLogo">a&r discocat</h2>
          <InstructionBar />
        </div>
        <DiscoveryInput inputValue={discoveryInput} setInputValue={setDiscoveryInput} save={saveCall}/>
        <div className="card">
          <h4>Artist List</h4>
          <p id="inputex">Please give it a moment to load when adding new artists</p>
          <ArtistList currentArtists={currentArtists} first={first} onPageChange={onPageChange} />
        </div>
      </div>
    </>
  )
}

export default App
