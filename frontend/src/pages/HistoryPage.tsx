import NavBar from "../components/NavBar";
import { useContext, useState } from "react";
import { SongsContext } from "../SongsContext";
import SongListItem from "../components/SongListItem";
import "../styles/Tabs.css";
import SongTabs from "../components/SongTabs";

function HistoryPage() {
  const songsContext = useContext(SongsContext);
  const { songs, setSongs } = songsContext!;
  const [searchQuery, setSearchQuery] = useState("");

  return (
    <>
      <NavBar curPage="history" />
      {/* <h1>History</h1> */}
      <div>
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
          flexDirection: "row",
          justifyContent: "center",
        }}
      >
        <div className="listBox">
          {songs
            .filter((s) => {
              if (
                searchQuery == "" ||
                s.title.toLowerCase().includes(searchQuery)
              ) {
                return s;
              }
            })
            .map((s) => (
              <SongListItem song={s} />
            ))}
        </div>
        <SongTabs />
      </div>
    </>
  );
}

export default HistoryPage;
