import NavBar from "../components/NavBar";
import "../styles/App.css";
import SongTabs from "../components/SongDisplayBox";
import SongListBox from "../components/SongListBox";

function HistoryPage() {
  return (
    <div>
      <NavBar curPage="history"/>
      <div className="history-title">
        <h1>Song History</h1>
      </div>
      <div className="history-con">
        <SongListBox/>
        <SongTabs/>
      </div>
    </div>
  );
}

export default HistoryPage;
