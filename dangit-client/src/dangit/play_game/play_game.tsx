import * as React from "react";
import gql from "graphql-tag";
import DocumentTitle from "react-document-title";
import { Mutation, MutationFn } from "react-apollo";
import { Section, Container, Heading } from "react-bulma-components";
import { Error } from "../error";
import { QuickQuery } from "../../quick_graphql";
import { Minefield, MinefieldAction } from "./minefield";

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
      board {
        openmap
        flagmap
      }
      open
      won
      startedAt
      finishedAt
    }
  }
`;

const MAKE_MOVE = gql`
  mutation makeMove($id: Int!, $position: Int!, $action: CellActionType!) {
    makeMove(id: $id, position: $position, action: $action) {
      ok
      gameState {
        board {
          openmap
          flagmap
        }
        open
        won
        startedAt
      }
    }
  }
`;

interface IPlayGameProps {
  id: string;
}

export class PlayGame extends React.Component<IPlayGameProps, {}> {
  public onCellAction(position: number, action: MinefieldAction, makeMove: MutationFn) {
    makeMove({variables: {position, action, id: this.props.id}});
  }

  public render() {
    return <DocumentTitle title={`Dangit! Play Game ${this.props.id}`}>
      <Section>
        <Container>
          <Heading>Game Time.</Heading>
          <QuickQuery query={GET_GAME_STATE} variables={{id: this.props.id}}>
            {(data) => {
              return <Mutation mutation={MAKE_MOVE}>
                {(makeMove, mutationData) => {
                  if (mutationData.error || (mutationData.data && !mutationData.data.makeMove.ok)) {
                    return <Error text="There was an internal error making a move. Sorry!"/>;
                  }

                  return <Minefield
                    rows={data.gameState.gameType.rows}
                    columns={data.gameState.gameType.columns}
                    openmap={new Set(mutationData.data && mutationData.data.makeMove.gameState.board.openmap || data.gameState.board.openmap)}
                    flagmap={new Set(mutationData.data && mutationData.data.makeMove.gameState.board.openmap || data.gameState.board.flagmap)}
                    actionCallback={(position, action) => this.onCellAction(position, action, makeMove) }
                  />;
              }}
            </Mutation>;
            }}
          </QuickQuery>
        </Container>
      </Section>
    </DocumentTitle>;
  }
}
