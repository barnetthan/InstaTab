import { ReactElement } from "react";
import "../styles/Tabs.css";
import { Song, Tab } from "../types/types";

interface GuitarTabProps {
  song: Song;
}

function GuitarTab({ song }: GuitarTabProps) {
  function createTabs() {
    const arr: ReactElement[] = [];
    const strings: string[] = ["E", "B", "G", "D", "A", "E"];
    const maxNotesPerLine = 25;

    // Create the base line with dashes
    let line = "";
    for (let i = 0; i <= song.maxTime; i++) {
      line += "―";
    }

    let curIndex = 0;
    let lines: string[] = [];

    // Generate lines for each string
    for (let i = 0; i < 6; i++) {
      let curLine = line;

      // Place frets on the correct positions in the line for each tab
      while (curIndex < song.tabs.length && song.tabs[curIndex].string === i) {
        const curTab: Tab = song.tabs[curIndex];
        curLine =
          curLine.substring(0, curTab.time) +
          curTab.fret +
          curLine.substring(curTab.time + 1);
        curIndex++;
      }
      lines.push(curLine);
    }

    // Chunk each string line into segments of 25 characters
    for (
      let chunkStart = 0;
      chunkStart < song.maxTime;
      chunkStart += maxNotesPerLine
    ) {
      for (let i = 0; i < 6; i++) {
        const curLineChunk = lines[i].substring(
          chunkStart,
          chunkStart + maxNotesPerLine
        );
        const lineWithStringMarker = strings[i] + " " + curLineChunk;

        // Render each character in the line as a span element
        for (let j = 0; j < lineWithStringMarker.length; j++) {
          arr.push(
            <span className="tabBox" key={`${i}-${chunkStart}-${j}`}>
              {lineWithStringMarker[j]}
            </span>
          );
        }
        arr.push(<br key={`linebreak-${i}-${chunkStart}`} />); // Break for each string line
      }
      arr.push(<br />);
      arr.push(<br key={`sectionbreak-${chunkStart}`} />); // Add an extra break between sections of 25 notes
    }

    return arr;
  }

  return <>{createTabs()}</>;
}

export default GuitarTab;
