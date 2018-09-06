import * as React from "react";
import gql from "graphql-tag";
import { Link, Redirect } from "react-router-dom";
import { Section, Notification, Modal, Button, Box, Heading, Form } from "react-bulma-components";
import { QuickMutation } from "../../quick_graphql";
import { ModalButton } from "../modal_button";

const LOGIN = gql`
  mutation login($email: String!, $password: String!) {
    login(email: $email, password: $password) {
      ok
      errors
      user {
        email
      }
    }
  }
`;

interface ILoginModalProps {
  modal?: ModalButton;
}

interface ILoginModalState {
  email: string;
  password: string;
}

export class LoginModal extends React.Component<ILoginModalProps, ILoginModalState> {
  public constructor(props: {}) {
    super(props);
    this.state = {
      email: "",
      password: "",
    };
  }

  public handleChange(fieldname: "email" | "password", event: React.FormEvent<HTMLInputElement>) {
    const stateUpdate: Partial<ILoginModalState> = {};
    stateUpdate[fieldname] = event.currentTarget.value || "";
    this.setState(stateUpdate as Pick<ILoginModalState, keyof ILoginModalState>);
  }

  public render() {
    return <Modal.Content>
        <Section>
          <QuickMutation mutation={LOGIN}>
            {(login, data) => {
              if (data && data.login.ok) {
                // hack to reload the page to reset cookies for django session
                // and to reset apollo cache for users. I tried for a while to get the modal to close nicely
                // and the queries to reload automatically, but it proved difficult, so I am cheating!
                // Sometimes, the elegant thing is a lot more dev time than the time it might save users.
                window.location.href = "/";
              }

              return <Box>
                <Heading>Login to Dangit!</Heading>
                {data && !data.login.ok && <Notification>Invalid username or passworrd</Notification>}
                <Form.Field>
                  <Form.Label>Email</Form.Label>
                  <Form.Control>
                    <Form.Input
                      type="email"
                      placeholder="Email"
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
                      value={this.state.password}
                      onChange={(e: React.FormEvent<HTMLInputElement>) => this.handleChange("password", e)}
                    />
                  </Form.Control>
                </Form.Field>

                <Button color="info" onClick={() => login({variables: this.state})}>Login</Button>
                <hr/>

                <p>Don't have an account? <Link to="/register" onClick={() => this.props.modal && this.props.modal.close()}>Sign up here</Link>.</p>
              </Box>;
            }}
          </QuickMutation>
        </Section>
      </Modal.Content>;
  }
}
