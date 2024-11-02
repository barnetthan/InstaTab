import { BrowserRouter, Route, Routes } from 'react-router-dom'
import HomePage from './pages/HomePage'
import HistoryPage from './pages/HistoryPage';
import AccountPage from './pages/AccountPage';
import "./styles/App.css";

function App() {
  return (
    <>
      <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/history" element={<HistoryPage />} />
        <Route path="/account" element={<AccountPage />} />
      </Routes>
      </BrowserRouter>
    </>
  )
}

export default App;
