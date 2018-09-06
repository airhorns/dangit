import * as React from "react";
import gql from "graphql-tag";
import DocumentTitle from "react-document-title";
import { Mutation, MutationFn } from "react-apollo";
import { Section, Container, Heading, Box } from "react-bulma-components";
import { Error } from "../error";
import { QuickQuery } from "../../quick_graphql";
import { Minefield, MinefieldAction } from "./minefield";
import { GameHeader } from "./game_header";

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
  mutation makeMove($id: Int!, $position: Int!, $action: MoveActionType!) {
    makeMove(id: $id, position: $position, action: $action) {
      ok
      gameState {
        id
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

interface IPlayGameState {
  enabled: boolean;
}

export class PlayGame extends React.Component<IPlayGameProps, IPlayGameState> {
  public constructor(props: IPlayGameProps) {
    super(props);
    this.state = {
      enabled: true,
    };
  }

  public onCellAction(position: number, action: MinefieldAction, openmap: Set<number>, makeMove: MutationFn) {
    const mutationData = {variables: {position, action, id: this.props.id}};
    switch (action) {
      case MinefieldAction.Flag:
        makeMove(mutationData); // Always toggle the flag of a cell
        break;
      case MinefieldAction.Open:
        // Only open a cell if it isn't already open
        if (!openmap.has(position)) {
          makeMove(mutationData);
        }
        break;
       default:
      throw new RangeError(`Unknown MinefieldAction: ${action}`);
     }
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

                  const openmap: Set<number> = new Set(data.gameState.board.openmap);
                  console.log(openmap);
                  const flagmap: Set<number> = new Set(data.gameState.board.flagmap);

                  return <Box>
                    <GameHeader open={data.gameState.open} won={data.gameState.won} gameType={data.gameState.gameType} />
                    <Minefield
                      rows={data.gameState.gameType.rows}
                      columns={data.gameState.gameType.columns}
                      openmap={openmap}
                      flagmap={flagmap}
                      actionCallback={(position, action) => {
                        if (data.gameState.open) {
                          this.onCellAction(position, action, openmap, makeMove);
                        }
                      }}
                    />
                  </Box>;
              }}
            </Mutation>;
            }}
          </QuickQuery>
        </Container>
      </Section>
    </DocumentTitle>;
  }
}
