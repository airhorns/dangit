import "bulma/css/bulma.css";
import * as React from "react";
import * as ReactDOM from "react-dom";
import { Root } from "./src/dangit";

document.addEventListener("DOMContentLoaded", () => {
  ReactDOM.render(<Root/>, document.body.appendChild(document.createElement("div")));
});
