import * as React from "react";
import { Link } from "react-router-dom";
import { Section, Modal, Button, Box, Heading, Form } from "react-bulma-components";

export class LoginRegisterModal extends React.Component {
  public render() {
    return <Modal.Content>
        <Section>
          <Box>
            <Heading>Login to Dangit!</Heading>
            <Form.Field>
              <Form.Label>Email</Form.Label>
              <Form.Control>
                <Form.Input type="email" placeholder="Email" />
              </Form.Control>
            </Form.Field>

            <Form.Field>
              <Form.Label>Password</Form.Label>
              <Form.Control>
                <Form.Input type="email" placeholder="Password" />
              </Form.Control>
            </Form.Field>

            <Button color="info">Login</Button>

            <hr/>

            <p>Don't have an account? <Link to="/register">Sign up here</Link>.</p>
          </Box>
        </Section>
      </Modal.Content>;
  }
}
