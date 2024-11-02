import NavBar from "../components/NavBar";
import { useState } from "react";

function HomePage() {
  const [link, setLink] = useState<string>("");

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
      </form>
    </>
  );
}

export default HomePage;
