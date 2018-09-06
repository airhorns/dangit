import * as React from "react";
import gql from "graphql-tag";
import { Link } from "react-router-dom";
import { Section, Container, Heading, Button, Icon, Level } from "react-bulma-components";
import { QuickQuery } from "../quick_graphql";
import { ModalButton } from "./modal_button";
import { LoginModal } from "./register";

const GET_USER_AND_STATS = gql`
query getUserAndStats {
  user {
    email
  }
}
`;

export class Home extends React.Component<{}, {}> {
  public render() {
    return <Section>
      <Container>
        <Heading>Welcome to Dangit!</Heading>
        <Heading subtitle>Challenge yourself to clear the field fast without blowing up.</Heading>
        <Level>
          <Level.Side>
            <QuickQuery query={GET_USER_AND_STATS}>
              {(data) => {
                if (data.user) {
                  return <Level.Item>
                    Signed in as {data.user.email}
                  </Level.Item>;
                } else {
                  return <React.Fragment>
                    <Level.Item>
                      <ModalButton size="large" color="info" text="Sign Up / Log In">
                        {(modal) => <LoginModal modal={modal}/>}
                      </ModalButton>
                    </Level.Item>
                    <Level.Item>
                      to start tracking your stats or start a
                    </Level.Item>
                  </React.Fragment>;
                }
              }}
            </QuickQuery>
            <Level.Item>
              <Button renderAs={Link} size="large" color="success" to="/new">
                <Icon icon=" fas fa-plus" />
                <span>New Game</span>
              </Button>
            </Level.Item>
          </Level.Side>
        </Level>
      </Container>
    </Section>;
  }
}
