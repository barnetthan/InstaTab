import { useContext, useState } from "react";
import { SongsContext } from "../SongsContext";
import "../styles/Tabs.css";
import SongListItem from "./SongListItem";

function SongListBox() {
  const songsContext = useContext(SongsContext);
  const { songs, faves, setFaves } = songsContext!;
  const [searchQuery, setSearchQuery] = useState("");
  const [showFaves, setShowFaves] = useState<boolean>(false);

  function clearFaves() {
    if (window.confirm("Are you sure you want to unfavorite all songs?")) {
      setFaves([]);
    }
  }

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "center" }}>
        <b>Search Songs</b>&nbsp;
        <input
          value={searchQuery}
          onChange={(e) => {
            setSearchQuery(e.target.value);
          }}
          type="text"
        />
      </div>
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          marginBottom: "-3vh",
          marginTop: "1vh",
        }}
      >
        <button
          style={{ cursor: "pointer" }}
          onClick={() => {
            setShowFaves(!showFaves);
          }}
        >
          {showFaves ? <>Show All</> : <>Show Favorites Only</>}
        </button>
        &nbsp; &nbsp;
        <button
          style={{ cursor: "pointer" }}
          onClick={clearFaves}
          disabled={faves.length == 0}
        >
          Clear All Favorites ({faves.length})
        </button>
      </div>
      <div className="listBox">
        {songs
          .filter((s) => {
            if (
              searchQuery == "" ||
              s.title.toLowerCase().includes(searchQuery)
            ) {
              if (!showFaves || faves.includes(s.id)) {
                return s;
              }
            }
          })
          .map((s) => (
            <SongListItem song={s} />
          ))}
      </div>
    </div>
  );
}

export default SongListBox;
