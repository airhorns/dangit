import * as React from "react";
import { MinefieldAction } from "./minefield";
import { Icon } from "react-bulma-components";

interface IMinefieldCellProps {
  position: number;
  open: boolean;
  flagged: boolean;
  mine: boolean;
  adjacentMines?: number;
  actionCallback: (position: number, action: MinefieldAction) => void;
}

export class MinefieldCell extends React.Component<IMinefieldCellProps, {}> {
  public render() {
    return <div
      className={`minefield-cell ${this.props.open && "minefield-cell__open" || ""} ${this.props.flagged && "minefield-cell__flagged" || ""}`}
      onClick={(_) => this.props.actionCallback(this.props.position, MinefieldAction.Open)}
      onContextMenu={(e) => { this.props.actionCallback(this.props.position, MinefieldAction.Flag); e.preventDefault(); } }
    >
      {this.props.mine && <Icon icon=" fas fa-bomb" />}
      {this.props.flagged && <Icon icon=" fas fa-flag" />}
      {this.props.open && !this.props.mine && (this.props.adjacentMines || "")}
    </div>;
  }
}
