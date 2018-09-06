import * as React from "react";
import gql from "graphql-tag";
import { QuickMutation } from "../../quick_graphql";
import { Error } from "../error";

const LOGOUT = gql`
mutation logout {
  logout {
    ok
  }
}
`;

export interface ILogoutButtonProps {
  className?: string;
}

export class LogoutButton extends React.Component<ILogoutButtonProps> {
  public render() {
    return <QuickMutation mutation={LOGOUT}>
      {(logout, data) => {
        if (data && data.logout) {
          if (data.logout.ok) {
            window.location.href = "/";
          } else {
            return <Error text="There was a problem logging you out."/>;
          }
        }

        return <a
          className={this.props.className}
          onClick={(_) => logout()}
          >
          Logout
        </a>;
      }}
    </QuickMutation>;
  }
}
