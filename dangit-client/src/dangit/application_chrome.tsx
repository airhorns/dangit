import * as React from "react";

export class ApplicationChrome extends React.Component<{}, {}> {
  public render() {
    return <React.Fragment>
      <nav className="navbar is-danger">
        <div className="navbar-brand">
          <a className="navbar-item" href="/" id="home">
            <img src="/static/images/dangit-logo-white.svg" alt="Dangit: try not to blow up!" />
          </a>
        </div>

        <div className="navbar-menu">
          <div className="navbar-start">
            <a className="navbar-item" href="/">
              Home
            </a>
            <div className="navbar-item has-dropdown is-hoverable">
              <a className="navbar-link" href="/docs/">
                Docs
              </a>
            </div>
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
