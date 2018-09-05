import * as React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { ApplicationChrome } from "./application_chrome";
import { Home } from "./home";
import { NoMatch } from "./no_match";
import { NewGameMenu } from "./new_game_menu";

export class Root extends React.Component<{}, {}> {
  public render() {
    return <Router>
      <ApplicationChrome>
          <Switch>
            <Route path="/" exact component={Home} />
            <Route path="/new" exact component={NewGameMenu} />
            <Route component={NoMatch} />
          </Switch>
      </ApplicationChrome>
    </Router>;
  }
}
