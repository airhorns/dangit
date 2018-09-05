import * as React from "react";
import DocumentTitle from "react-document-title";
import { Section, Container, Heading } from "react-bulma-components";

interface IPlayGameProps {
  id: string;
}

export class PlayGame extends React.Component<IPlayGameProps, {}> {

  public render() {
    return <DocumentTitle title={`Dangit! Play Game ${this.props.id}`}>
      <Section>
        <Container>
          <Heading>Game ID {this.props.id}</Heading>
        </Container>
      </Section>
    </DocumentTitle>;
  }
}
