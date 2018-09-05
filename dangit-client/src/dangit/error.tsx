import * as React from "react";
import { Heading, Notification } from "react-bulma-components";

export interface IErrorProps {
  text?: string;
}

export class Error extends React.Component<IErrorProps> {
  public render() {
    return <React.Fragment>
      <Heading>Oops.</Heading>
      <Notification color="danger">
        <Heading subtitle>There has been an internal error.</Heading>
        {this.props.text}
        <br/>
        Please refresh your page to try again.
      </Notification>
    </React.Fragment>;
  }
}
