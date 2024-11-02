import NavBar from "../components/NavBar";
import { useState } from "react";
import GuitarTab from "../components/GuitarTab";

export interface Song {
  tabs: Tab[];
  favorite: boolean;
  maxTime: number;
}

export interface Tab {
  string: number;
  time: number;
  fret: number;
}

function HomePage() {
  const [link, setLink] = useState<string>("");

  // Dummy data for testing
  const dummyTabs: Tab[] = [
    { string: 0, time: 77, fret: 3 },
    { string: 1, time: 3, fret: 5 },
    { string: 1, time: 2, fret: 0 },
    { string: 4, time: 1, fret: 2 },
    { string: 4, time: 0, fret: 3 },
    { string: 5, time: 5, fret: 0 },
  ];

  const dummySong: Song = {
    tabs: dummyTabs,
    favorite: false,
    maxTime: 80,
  };

  function handleSubmit() {
    // implicity validates the input
    const url = new URL(link);

    // call api endpoint with current link
    // ex: axios.get(`https://api.example.com/getdata/${link}`);

    setLink("");
  }

  return (
    <>
      <NavBar curPage="home" />
      <h1>Welcome to InstaTab!</h1>
      <p>
        Upload a YouTube link or mp3 file to tranform music into guitar tabs
        instantly!
      </p>
      <form>
        <label>Add Link:</label>
        <input
          type="url"
          value={link}
          onChange={(e) => {
            setLink(e.target.value);
          }}
          placeholder="https://www.example.com"
        />
        <button disabled={!link} onClick={handleSubmit}>
          Submit
        </button>
        <br/>
      </form>
      <GuitarTab song={dummySong} />
    </>
  );
}

export default HomePage;
