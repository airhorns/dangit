import "react-bulma-components/dist/react-bulma-components.min.css";
import "@fortawesome/fontawesome-free/js/all.js";
import * as React from "react";
import * as ReactDOM from "react-dom";
import { Root } from "./src/dangit";

document.addEventListener("DOMContentLoaded", () => {
  ReactDOM.render(<Root/>, document.body.appendChild(document.createElement("div")));
});
