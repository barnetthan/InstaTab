import NavBar from "../components/NavBar";
import "../styles/Tabs.css";
import SongTabs from "../components/SongDisplayBox";
import SongListBox from "../components/SongListBox";

function HistoryPage() {
  return (
    <div className="historypage">
      <NavBar curPage="history" />
      <div
        style={{
          display: "flex",
          justifyContent: "center",
        }}
      >
        <h1>Song History</h1>
      </div>
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          justifyContent: "center",
        }}
      >
        <SongListBox />
        <SongTabs />
      </div>
    </div>
  );
}

export default HistoryPage;
