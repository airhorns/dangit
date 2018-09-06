import * as React from "react";
import gql from "graphql-tag";
import { Link } from "react-router-dom";
import { QuickMutation } from "../../quick_graphql";
import DocumentTitle from "react-document-title";
import { Section, Columns, Button, Container, Notification, Heading, Box, Form, Icon } from "react-bulma-components";

const REGISTER = gql`
  mutation register($email: String!, $password: String!) {
    register(email: $email, password: $password) {
      ok
      errors
    }
  }
`;

interface IRegisterState {
  email: string;
  password: string;
}

export class Register extends React.Component<{}, IRegisterState> {
  public constructor(props: {}) {
    super(props);
    this.state = {
      email: "",
      password: "",
    };
  }

  public handleChange(fieldname: keyof IRegisterState, event: React.FormEvent<HTMLInputElement>) {
    const stateUpdate: Partial<IRegisterState> = {};
    stateUpdate[fieldname] = event.currentTarget.value || "";
    this.setState(stateUpdate as Pick<IRegisterState, keyof IRegisterState>);
  }

  public render() {
    return <DocumentTitle title="Register Account - Dangit!">
      <Section>
      <Container>
        <QuickMutation mutation={REGISTER}>
          {(register, data?) => {
            if (data) {
              if (data.register.ok) {
                return <Notification color="success">
                  <Heading>You have been registered!</Heading>
                  <Heading subtitle>You are now logged in. Thanks for joining Dangit.</Heading>
                  <Button renderAs={Link} size="large" to="/new">
                    <Icon icon=" fas fa-plus" />
                    <span>Start a Game</span>
                  </Button>
                </Notification>;
              }
            }

            return <React.Fragment>
              <Columns centered={true}>
                <Columns.Column  size="half">
                  <Heading>New Account Time!</Heading>
                  <Box>
                    {data && data.register.errors && <Notification color="danger">{data.register.errors.join(": ")}</Notification>}
                    <form onSubmit={() => register({variables: this.state})}>
                      <Form.Field>
                        <Form.Label>Email</Form.Label>
                        <Form.Control>
                          <Form.Input
                            type="email"
                            placeholder="Email"
                            required
                            value={this.state.email}
                            onChange={(e: React.FormEvent<HTMLInputElement>) => this.handleChange("email", e)}
                          />
                        </Form.Control>
                      </Form.Field>

                      <Form.Field>
                        <Form.Label>Password</Form.Label>
                        <Form.Control>
                          <Form.Input
                            type="password"
                            placeholder="Password"
                            required
                            value={this.state.password}
                            onChange={(e: React.FormEvent<HTMLInputElement>) => this.handleChange("password", e)}
                          />
                        </Form.Control>
                      </Form.Field>

                      <Button color="info">Register</Button>
                    </form>
                  </Box>
                </Columns.Column>
              </Columns>
            </React.Fragment>;
          }}
        </QuickMutation>
      </Container>
    </Section>
  </DocumentTitle>;
  }
}
