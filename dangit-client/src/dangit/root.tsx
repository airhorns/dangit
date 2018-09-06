import * as React from "react";
import * as Cookies from "js-cookie";
import DocumentTitle from "react-document-title";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { ApolloClient } from "apollo-client";
import { InMemoryCache } from "apollo-cache-inmemory";
import { HttpLink } from "apollo-link-http";
import { onError } from "apollo-link-error";
import { ApolloLink } from "apollo-link";
import { ApolloProvider } from "react-apollo";

import { ApplicationChrome } from "./application_chrome";
import { Home } from "./home";
import { NoMatch } from "./no_match";
import { NewGameMenu } from "./new_game_menu";
import { PlayGame } from "./play_game";
import { Register } from "./register";

const csrfInput = document.querySelector("input[name=csrfmiddlewaretoken]") as HTMLInputElement;
const csrfToken = csrfInput && csrfInput.value || null;

const client = new ApolloClient({
  link: ApolloLink.from([
    onError(({ graphQLErrors, networkError }) => {
      if (graphQLErrors) {
        graphQLErrors.map(({ message, locations, path }) =>
          console.log(                                                        // tslint:disable-line
            `[GraphQL error]: Message: ${message}`,
            {locations, path},
          ),
        );
      }
      if (networkError) { console.log(`[Network error]: ${networkError}`); }  // tslint:disable-line
    }),
    new HttpLink({
      uri: "/graphql",
      credentials: "same-origin",
      headers: {
          "X-CSRFToken": Cookies.get("csrftoken"),
      },
    }),
  ]),
  cache: new InMemoryCache(),
});

export class Root extends React.Component<{}, {}> {
  public render() {
    return <DocumentTitle title="Dangit!">
      <ApolloProvider client={client}>
        <Router>
          <ApplicationChrome>
              <Switch>
                <Route path="/" exact component={Home} />
                <Route path="/new" exact component={NewGameMenu} />
                <Route path="/game/:id" render={({match}) => <PlayGame id={match.params.id}/>}/>
                <Route path="/register" exact component={Register}/>
                <Route component={NoMatch} />
              </Switch>
          </ApplicationChrome>
        </Router>
      </ApolloProvider>
    </DocumentTitle>;
  }
}
