import * as React from "react";
import gql from "graphql-tag";
import DocumentTitle from "react-document-title";
import { Section, Container, Heading } from "react-bulma-components";
import { QuickQuery } from "../../quick_graphql";

const GET_GAME_STATE = gql`
  query getGameState($id: Int!) {
    gameState(id: $id) {
      id
      gameType {
        rows
        columns
        mines
        name
      }
      open
      won
      startedAt
      finishedAt
    }
  }
`;

interface IPlayGameProps {
  id: string;
}

export class PlayGame extends React.Component<IPlayGameProps, {}> {
  public render() {
    return <DocumentTitle title={`Dangit! Play Game ${this.props.id}`}>
      <Section>
        <Container>
          <Heading>Game Time.</Heading>
          <QuickQuery query={GET_GAME_STATE} variables={{id: this.props.id}}>
            {(data) => {
              return <p>{JSON.stringify(data)}</p>;
            }}
          </QuickQuery>
        </Container>
      </Section>
    </DocumentTitle>;
  }
}
