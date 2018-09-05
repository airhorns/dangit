import * as React from "react";
import { Mutation, MutationProps, MutationFn, MutationResult } from "react-apollo";
import { Error } from "../dangit/error";

export interface IQuickMutationProps extends MutationProps {
  children: (mutate: MutationFn, data?: any) => React.ReactNode | null;
}

// Handy class for automatically handling the loading and error states of a mutation in a generic way
// Wraps the children function of Apollo's Mutation component to return just the data and always the data
// to avoid checking for loading, errors, and data presence every time.
// Could be extended to have customizeable loading and error messages, or be configurable so it could be turned
// into a reusable library. For now, couple directly to this app for speed.
export class QuickMutation extends React.Component<IQuickMutationProps, {}> {
  public render() {
    const children = this.props.children;
    const quickChildren = (mutate: MutationFn, result: MutationResult) => {
      if (result.loading) {
        return "Loading...";
      }
      if (result.error) {
        return <Error text="There was an error communicating with the server."/>;
      }

      return children(mutate, result.data);
    };

    const props = Object.assign({}, this.props, {children: quickChildren});

    return <Mutation {...props}/>;
  }
}
