import * as React from "react";
import { MinefieldAction } from "./minefield";

interface IMinefieldCellProps {
  position: number;
  open: boolean;
  flagged: boolean;
  contents: string;
  actionCallback: (position: number, action: MinefieldAction) => void;
}

export class MinefieldCell extends React.Component<IMinefieldCellProps, {}> {
  public render() {
    return <div
      className={`minefield-cell ${this.props.open && "minefield-cell__open"} ${this.props.flagged && "minefield-cell__flagged"}`}
      onClick={(_) => this.props.actionCallback(this.props.position, MinefieldAction.Open)}
      onContextMenu={(e) => { this.props.actionCallback(this.props.position, MinefieldAction.Flag); e.preventDefault(); } }
    >
      {this.props.contents}
    </div>;
  }
}
