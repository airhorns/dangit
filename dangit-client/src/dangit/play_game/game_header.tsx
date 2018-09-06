import * as React from "react";
import { Link } from "react-router-dom";
import { Tag, Form } from "react-bulma-components";

interface IGameHeaderProps {
  open: boolean;
  won: boolean;
  gameType: {
    name: string;
  };
}

export class GameHeader extends React.Component<IGameHeaderProps, {}> {
  public colorForStatus() {
    if (this.props.open) {
      return "primary";
    } else {
      if (this.props.won) {
        return "success";
      } else {
        return "danger";
      }
    }
  }

  public statusText() {
    if (this.props.open) {
      return "Game time";
    } else {
      if (this.props.won) {
        return "Winner!";
      } else {
        return "Exploded";
      }
    }
  }

  public render() {
    return <Form.Field multiline kind="group">
      <Form.Control>
        <Tag.Group gapless>
          <Tag color="dark">Mode</Tag>
          <Tag color="info">{this.props.gameType.name}</Tag>
        </Tag.Group>
      </Form.Control>
      <Form.Control>
        <Tag.Group gapless>
          <Tag color="dark">Status</Tag>
          <Tag color={this.colorForStatus()}>{this.statusText()}</Tag>
        </Tag.Group>
      </Form.Control>
      {!this.props.open && <Form.Control>
        <Link to="/new">Play again?</Link>
      </Form.Control>}
    </Form.Field>;
  }
}
