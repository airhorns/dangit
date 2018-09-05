import * as React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { ApplicationChrome } from "./application_chrome";
import { Home } from "./home";
import { NoMatch } from "./no_match";

export class Root extends React.Component<{}, {}> {
  public render() {
    return <Router>
      <ApplicationChrome>
          <Switch>
            <Route path="/" exact component={Home} />
            <Route component={NoMatch} />
          </Switch>
      </ApplicationChrome>
    </Router>;
  }
}
