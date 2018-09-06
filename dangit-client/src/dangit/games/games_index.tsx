import * as React from "react";
import gql from "graphql-tag";
import { Link } from "react-router-dom";
import { Section, Container, Heading, Table } from "react-bulma-components";
import { WinTag } from "./win_tag";
import { QuickQuery } from "../../quick_graphql";

const GET_GAME_STATES = gql`
query getGameStates {
  allGameStates {
    id
    won
    open
    gameType {
      name
    }
    startedAt
    finishedAt
  }
}
`;

export class GamesIndex extends React.Component<{}, {}> {
  public render() {
    return <Section>
      <Container>
        <Heading>Games</Heading>
        <QuickQuery query={GET_GAME_STATES}>
          {(data) => {
            const rows = data.allGameStates.map((gameState: any) => <tr>
              <td>{gameState.startedAt}</td>
              <td>{gameState.finishedAt}</td>
              <td>{gameState.gameType.name}</td>
              <td><WinTag won={gameState.won}/></td>
              <td><Link to={`/game/${gameState.id}`}>View</Link></td>
            </tr>);
            return <Table>
              <thead>
                <tr>
                  <th>Started At</th>
                  <th>Finished At</th>
                  <th>Game Type</th>
                  <th>Won?</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {rows}
              </tbody>
            </Table>;
          }}
        </QuickQuery>
      </Container>
    </Section>;
  }
}
