import NavBar from "../components/NavBar";
import { useContext } from 'react';
import { SongsContext } from '../SongsContext';

function FavoritesPage() {
  const songsContext = useContext(SongsContext);
  const { songs, setSongs } = songsContext!;

  return (
    <>
      <NavBar curPage="favorites"/>
      <h1>Favorites Page!</h1>
      {songs.map((s) => (
        <div>{s.title}</div>
      ))}
    </>
  )
}

export default FavoritesPage;
