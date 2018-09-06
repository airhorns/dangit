import * as React from "react";
import gql from "graphql-tag";
import { Redirect } from "react-router-dom";
import { QuickMutation } from "../../quick_graphql";
import DocumentTitle from "react-document-title";
import { Section, Container, Heading, Tile } from "react-bulma-components";
import { GameTypeTile } from "./game_type_tile";
import { Error } from "../error";

const START_GAME = gql`
  mutation startGame($gameType: String!) {
    startGame(gameType: $gameType) {
      ok
      gameState {
        id
      }
    }
  }
`;

const GAME_TYPES = [
  {
    name: "beginner",
    description: "Start off mild with a 10 mine game.",
    color: "primary",
  }, {
    name: "intermediate",
    description: "Make things interesting at a 50 mine game.",
    color: "info",
  }, {
    name: "expert",
    description: "Challenge yourself to find all 99 mines!",
    color: "danger",
  },
];

const capitalizeFirstLetter = (str: string) => {
    return str.charAt(0).toUpperCase() + str.slice(1);
};

export class NewGameMenu extends React.Component<{}, {}> {
  public render() {
    return <DocumentTitle title="Dangit! New Game">
      <Section>
      <Container>
        <QuickMutation mutation={START_GAME}>
          {(startGame, data?) => {
            if (data) {
              if (data.startGame.ok) {
                return <Redirect push to={`/game/${data.startGame.gameState.id}`}/>;
              } else {
                return <Error text="We're unable to start new games right now."/>;
              }
            }

            const gameTiles = GAME_TYPES.map(({name, description, color}) => {
              return <GameTypeTile
                title={capitalizeFirstLetter(name)}
                key={name}
                color={color}
                description={description}
                startCallback={(_) => startGame({variables: {gameType: name}})}
              />;
            });

            return <React.Fragment>
              <Heading>New Game Time!</Heading>
              <Tile kind="ancestor">
                {gameTiles}
              </Tile>
            </React.Fragment>;
          }}
        </QuickMutation>
      </Container>
    </Section>
  </DocumentTitle>;
  }
}
