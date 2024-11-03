import { createContext, useState, useEffect, ReactNode } from 'react';
import { Song } from './types/types.ts';

// Define the shape of the context
interface SongsContextProps {
  songs: Song[];
  setSongs: React.Dispatch<React.SetStateAction<Song[]>>;
  faves: number[];
  setFaves: React.Dispatch<React.SetStateAction<number[]>>;
  cur: Song | null;
  setCur: Function;
}

// Create the context with a default value (can be empty here)
export const SongsContext = createContext<SongsContextProps | undefined>(undefined);

// Create the provider component
export const SongsProvider = ({ children }: { children: ReactNode }) => {
  const dummyTabs = [
    { string: 0, time: 77, fret: 3 },
    { string: 1, time: 3, fret: 5 },
    { string: 1, time: 2, fret: 0 },
    { string: 4, time: 1, fret: 2 },
    { string: 4, time: 0, fret: 3 },
    { string: 5, time: 5, fret: 0 },
  ];

  const dummySong: Song = {
    tabs: dummyTabs,
    favorite: false,
    maxTime: 80,
    title: "Skeletons by Keshi",
    id: 0,
  };

  const [songs, setSongs] = useState<Song[]>(() => {
    const storedSongs = localStorage.getItem("songs");
    return storedSongs ? JSON.parse(storedSongs) : [dummySong];
  });

  const [faves, setFaves] = useState<number[]>(() => {
    const storedFaves = localStorage.getItem("faveSongs");
    return storedFaves ? JSON.parse(storedFaves) : [];
  });

  const [cur, setCur] = useState<Song | null>(null);

  // Save songs to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem("songs", JSON.stringify(songs));
  }, [songs]);

  return (
    <SongsContext.Provider value={{ songs, setSongs, faves, setFaves, cur, setCur }}>
      {children}
    </SongsContext.Provider>
  );
};
