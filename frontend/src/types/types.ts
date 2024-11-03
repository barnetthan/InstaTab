export interface Song {
  tabs: Tab[];
  maxTime: number;
  title: string;
  id: number;
}

export interface Tab {
  string: number;
  time: number;
  fret: number;
}