import "../styles/Tabs.css";
import { FaRegStar, FaStar } from "react-icons/fa"; // Font Awesome
import { useContext } from "react";
import { SongsContext } from "../SongsContext";
import { Song } from "../types/types";

interface SongListItemProps {
  song: Song;
}

function SongListItem({ song }: SongListItemProps) {
  const songsContext = useContext(SongsContext);
  const { faves, setFaves, cur, setCur } = songsContext!;

  function handleFavorite() {
    let arr = [...faves];
    if (!arr.includes(song.id)) {
      arr.push(song.id);
    } else {
      arr.splice(arr.indexOf(song.id), 1);
    }
    setFaves(arr);
    localStorage.setItem("faveSongs", JSON.stringify(arr));
  }

  return (
    <div
      className="listItem"
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        backgroundColor: cur && cur.id == song.id ? "lightgray" : "white",
      }}
    >
      <div
        style={{ fontWeight: cur && cur.id == song.id ? "bolder" : "normal" }}
      >
        {song.title}
      </div>
      <div
        style={{ display: "flex", alignItems: "center", marginRight: "10px" }}
      >
        <div
          style={{ cursor: "pointer", marginRight: "10px" }}
          onClick={handleFavorite}
        >
          {faves.includes(song.id) ? <FaStar /> : <FaRegStar />}
        </div>
        &nbsp;
        <button
          style={{ cursor: "pointer" }}
          onClick={() => {
            setCur(song);
          }}
        >
          View
        </button>
      </div>
    </div>
  );
}

export default SongListItem;
