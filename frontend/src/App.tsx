import { BrowserRouter, Route, Routes } from 'react-router-dom'
import HomePage from './pages/HomePage'
import HistoryPage from './pages/HistoryPage';
import "./styles/App.css";
import { SongsProvider } from './SongsContext';

function App() {

  return (
    <SongsProvider>
      <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/history" element={<HistoryPage />} />
      </Routes>
      </BrowserRouter>
    </SongsProvider>
  )
}

export default App;
