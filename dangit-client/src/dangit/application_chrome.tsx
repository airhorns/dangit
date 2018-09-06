import * as React from "react";
import gql from "graphql-tag";
import { NavLink } from "react-router-dom";
import { QuickQuery } from "../quick_graphql";
import { ModalButton } from "./modal_button";
import { LoginModal, LogoutButton } from "./register";

const LOGGED_IN = gql`
  query getUser {
    user {
      email
    }
  }
`;

export class ApplicationChrome extends React.Component<{}, {burgerOpen: boolean}> {
  constructor(props: {}) {
    super(props);
    this.state = {
      burgerOpen: false,
    }
  }

  public render() {
    return <React.Fragment>
      <nav className="navbar is-danger">
        <div className="navbar-brand">
          <a className="navbar-item" href="/" id="home">
            <img src="/static/images/dangit-logo-white.svg" alt="Dangit: try not to blow up!" />
          </a>

          <a
            role="button"
            className={`navbar-burger ${this.state.burgerOpen && "is-active"}`}
            aria-label="menu"
            onClick={(_) => this.setState((state) => ({burgerOpen: !state.burgerOpen}))}
          >
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
          </a>
        </div>

        <div className={`navbar-menu ${this.state.burgerOpen && "is-active"}`}>
          <div className="navbar-start">
            <NavLink className="navbar-item" to="/new">New Game</NavLink>
          </div>
          <div className="navbar-end">
            <QuickQuery query={LOGGED_IN}>
              {(data) => {
                if (data.user) {
                  return <LogoutButton className="navbar-item"/>;
                } else {
                  return <ModalButton renderAsLink={true} className="navbar-item" text="Log In">
                    {(modal) => <LoginModal modal={modal}/>}
                  </ModalButton>;
                }
              }}
            </QuickQuery>
          </div>
        </div>
      </nav>

      {this.props.children}

      <footer className="footer">
        <div className="content has-text-centered">
          <p>
            <strong>Dangit</strong> by <a href="https://harry.me">Harry Brundage</a>
            . <a href="https://github.com/airhorns/dangit">Source code</a> is licensed <a href="http://opensource.org/licenses/mit-license.php">MIT</a>.
          </p>
        </div>
      </footer>
    </React.Fragment>;
  }
}
