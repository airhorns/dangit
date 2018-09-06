import * as React from "react";
import { MinefieldCell } from "./minefield_cell";
import { MinefieldRow } from "./minefield_row";
import "./minefield.css";

export enum MinefieldAction {
  Open = "OPEN",
  Flag = "FLAG",
}

export interface IAdjacentMineCounts {
  [key: number]: number;
}

interface IMinefieldProps {
  gameType: {
    name: string;
    rows: number;
    columns: number;
  };
  openmap: Set<number>;
  flagmap: Set<number>;
  minemap?: Set<number>;
  adjacentMineCounts: IAdjacentMineCounts;
  actionCallback: (position: number, action: MinefieldAction) => void;
}

const range = (upto: number) => Array.from(Array(upto).keys());

export class Minefield extends React.Component<IMinefieldProps, {}> {
  public render() {
    const rows = range(this.props.gameType.rows).map((row) => {
      const cells = range(this.props.gameType.columns).map((column) => {
        const position = (row * this.props.gameType.columns) + column;
        return <MinefieldCell
          key={position}
          position={position}
          adjacentMines={this.props.adjacentMineCounts[position]}
          actionCallback={this.props.actionCallback}
          open={this.props.openmap.has(position)}
          flagged={this.props.flagmap.has(position)}
          mine={!!(this.props.minemap && this.props.minemap.has(position))}
        />;
      });

      return <MinefieldRow key={row}>{cells}</MinefieldRow>;
    });

    return <div className={`minefield ${this.props.gameType.name.includes("hexagonal") && "minefield__hexagonal"}`}>
      {rows}
    </div>;
  }
}
