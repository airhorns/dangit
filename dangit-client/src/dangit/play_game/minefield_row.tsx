import * as React from "react";

export class MinefieldRow extends React.Component<{}, {}> {
  public render() {
    return <div className="minefield-row">
      {this.props.children}
    </div>;
  }
}
