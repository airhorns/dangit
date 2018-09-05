import * as React from "react";
import { Button, Icon, Tile } from "react-bulma-components";

export interface IGameTypeTileProps {
  color: string;
  title: string;
  description: string;
  startCallback: (event: React.UIEvent) => void;
}

export class GameTypeTile extends React.Component<IGameTypeTileProps> {

  public render() {
    return <Tile kind="parent">
      <Tile kind="child" notification color={this.props.color}>
        <p className="title">{this.props.title}</p>
        <p>{this.props.description}</p>
        <p>
          <Button onClick={this.props.startCallback}><Icon icon=" fas fa-bomb"/><span>Start</span></Button>
        </p>
      </Tile>
    </Tile>;
  }
}
