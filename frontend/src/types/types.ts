export interface Song {
  tabs: Tab[];
  favorite: boolean;
  maxTime: number;
  title: string;
  id: number;
}

export interface Tab {
  string: number;
  time: number;
  fret: number;
}