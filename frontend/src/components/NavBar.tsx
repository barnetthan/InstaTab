import { NavLink } from "react-router-dom";
import "../styles/App.css";
// import "@fontsource/roboto/400.css";

interface NavBarProps {
  curPage: string;
}

export default function NavBar({ curPage }: NavBarProps) {
  return (
    <nav>
      <a href="/">
        <h1>InstaTab</h1>
      </a>
      <ul>
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
      </ul>
    </nav>
  );
}
