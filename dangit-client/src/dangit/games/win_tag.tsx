import * as React from "react";
import { Tag, Icon } from "react-bulma-components";

export interface IWinTagProps {
  won: true | false | null;
}

export class WinTag extends React.Component<IWinTagProps> {
  public render() {
    let color: string;
    let text: string | JSX.Element;

    if (this.props.won === null) {
      color = "warning";
      text = "Unfinished";
    } else if (this.props.won) {
      color = "success";
      text = "Winner!";
    } else {
      color = "danger";
      text = <Icon icon=" fas fa-bomb" />;
    }

    return <Tag color={color}>{text}</Tag>;
  }
}
