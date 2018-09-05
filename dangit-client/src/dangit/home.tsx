import * as React from "react";
import { Section, Container, Heading, Button, Icon, Level } from "react-bulma-components";

export class Home extends React.Component<{}, {}> {
  public render() {
    return <Section>
      <Container>
        <Heading>Welcome to Dangit!</Heading>
        <Heading subtitle>Challenge yourself to clear the field fast without blowing up.</Heading>
        <Level>
          <Level.Side>
            <Level.Item>
              <Button size="large" color="success">
                <Icon icon=" fas fa-plus" />
                <span>New Game</span>
              </Button>
            </Level.Item>
            <Level.Item>
              or
            </Level.Item>
            <Level.Item>
              <Button size="large" color="info">
                Sign Up / Log In
              </Button>
            </Level.Item>
            <Level.Item>
              to start tracking your stats.
            </Level.Item>
          </Level.Side>
        </Level>
      </Container>
    </Section>;
  }
}
