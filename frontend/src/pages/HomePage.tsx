import NavBar from "../components/NavBar";
import { useState } from "react";
import { Song } from "../types/types";
import { useContext } from "react";
import { SongsContext } from "../SongsContext";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function HomePage() {
  const [link, setLink] = useState<string>("");
  const [title, setTitle] = useState<string>("");
  const songsContext = useContext(SongsContext);
  const { songs, setSongs, setCur } = songsContext!;

  const navigate = useNavigate();

  const dummyTabs = [
    { string: 0, time: 27, fret: 3 },
    { string: 1, time: 3, fret: 5 },
    { string: 1, time: 2, fret: 0 },
    { string: 4, time: 1, fret: 2 },
    { string: 4, time: 0, fret: 3 },
    { string: 5, time: 5, fret: 0 },
  ];

  const fetchAPI = async () => {
    const response = await axios.get("http://localhost:60000/api/songs");
    console.log(response.data.tabs[0].string);


    let id = 0;
    if (songs.length > 0) {
      id = songs[songs.length - 1].id + 1;
    }

    const newSong: Song = {
      tabs: response.data.tabs,
      maxTime: response.data.maxTime,
      title: title.length > 0 ? title : "Untitled Song 69420 " + id,
      id: id,
    };
    setSongs([...songs, newSong]);
    setCur(newSong);
    // setArray(response.data.songs);
  }

  function handleSubmit() {
    // implicity validates the input
    const url = new URL(link);

    // call api endpoint with current link
    // ex: axios.get(`https://api.example.com/getdata/${link}`);

    // let id = 0;
    // if (songs.length > 0) {
    //   id = songs[songs.length - 1].id + 1;
    // }

    // const newSong: Song = {
    //   tabs: dummyTabs,
    //   maxTime: 40,
    //   title: title.length > 0 ? title : "Untitled Song " + id,
    //   id: id,
    // };

    // setSongs([...songs, newSong]);
    fetchAPI();

    setLink("");
    setTitle("");
    navigate("/history");
  }

  return (
    <div className="homepage">
      <NavBar curPage="home" />
      <h1>Welcome to InstaTab!</h1>
      <p>
        Upload a YouTube link or MP3 file to tranform music into guitar tabs
        instantly!
      </p>
      <form className="homepage">
        <label>Song Title:</label>
        &nbsp;
        <input
          className="titleForm"
          type="text"
          value={title}
          onChange={(e) => {
            setTitle(e.target.value);
          }}
          placeholder="Best Song Ever!"
        />
        &nbsp;
        <label>Link:</label>
        &nbsp;
        <input
          className="urlForm"
          type="url"
          value={link}
          onChange={(e) => {
            setLink(e.target.value);
          }}
          placeholder="https://www.example.com"
        />
        &nbsp;
        <button disabled={!link} onClick={handleSubmit}>
          Submit
        </button>
        <br />
      </form>
      {/* {array.map((s) => (<div>{s}</div>))} */}
      <button onClick={fetchAPI}>GET DATA BABYY</button>
    </div>
  );
}

export default HomePage;
