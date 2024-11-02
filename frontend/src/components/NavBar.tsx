import { NavLink } from "react-router-dom";
import "../styles/NavBar.css";
// import "@fontsource/roboto/400.css";

interface NavBarProps {
  curPage: string;
}

export default function NavBar({ curPage } : NavBarProps) {

  return (
    <nav className="nav">
      <a href="/">
        <h1>InstaTab</h1>
      </a>
      <ul style={{ marginRight: 50 }}>
        <li className="special">
          <NavLink
            className="uladjust"
            style={{
              textDecorationLine: curPage == "home" ? "underline" : "none",
            }}
            to="/"
          >
            Home
          </NavLink>
        </li>
        <li>
          <NavLink
            className="uladjust"
            style={{
              textDecorationLine: curPage == "history" ? "underline" : "none",
            }}
            to="/history"
          >
            History
          </NavLink>
        </li>
        <li>
          <NavLink
            className="uladjust"
            style={{
              textDecorationLine: curPage == "account" ? "underline" : "none",
            }}
            to="/account"
          >
            Account
          </NavLink>
        </li>
      </ul>
    </nav>
  );
}