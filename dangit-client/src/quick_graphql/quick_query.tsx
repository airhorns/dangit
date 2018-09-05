import * as React from "react";
import { Query, QueryProps, QueryResult } from "react-apollo";
import { Error } from "../dangit/error";

export interface IQuickQueryProps extends QueryProps {
  children: (data: any) => React.ReactNode | null;
}

// Handy class for automatically handling the loading and error states of a Query in a generic way
// Wraps the children function of Apollo's Query component to return just the data and always the data
// to avoid checking for loading, errors, and data presence every time.
// Could be extended to have customizeable loading and error messages, or be configurable so it could be turned
// into a reusable library. For now, couple directly to this app for speed.
export class QuickQuery extends React.Component<IQuickQueryProps, {}> {
  public render() {
    const children = this.props.children;
    const quickChildren = (result: QueryResult) => {
      if (result.loading) {
        return "Loading...";
      }
      if (result.error) {
        return <Error text="There was an error communicating with the server."/>;
      }

      return children(result.data);
    };

    const props = Object.assign({}, this.props, {children: quickChildren});

    return <Query {...props}/>;
  }
}
