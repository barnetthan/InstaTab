import { useContext } from "react";
import { SongsContext } from "../SongsContext";
import GuitarTab from "./GuitarTab";
import "../styles/App.css";

function SongDisplayBox() {
  const songsContext = useContext(SongsContext);
  const { cur } = songsContext!;

  return (
    <div className="infoBox">
      {cur ? (
        <>
          <h2>Guitar Tabs for {cur.title}</h2>
          <GuitarTab song={cur} />
        </>
      ) : (
        <h1>No Song Selected.</h1>
      )}
    </div>
  );
}

export default SongDisplayBox;
