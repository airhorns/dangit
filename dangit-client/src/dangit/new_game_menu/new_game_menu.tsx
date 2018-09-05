import * as React from "react";
import { Section, Container, Heading, Tile } from "react-bulma-components";
import { GameTypeTile } from "./game_type_tile";

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
  public startGame(gameType: string) {

  }

  public render() {
    const gameTiles = GAME_TYPES.map(({name, description, color}) => {
      return <GameTypeTile
        title={capitalizeFirstLetter(name)}
        color={color}
        description={description}
        startCallback={(_) => this.startGame(name)}
      />
    });

    return <Section>
      <Container>
        <Heading>New Game Time!</Heading>
        <Tile kind="ancestor">
          {gameTiles}
        </Tile>
      </Container>
    </Section>;
  }
}
