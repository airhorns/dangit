import * as React from "react";
import { Button, Modal } from "react-bulma-components";
export { Modal } from "react-bulma-components";

export interface IModalButtonProps {
  size?: string;
  color?: string;
  text: string;
  modalProps?: any;
}

export interface IModalButtonState {
  show: boolean;
}

export class ModalButton extends React.Component<IModalButtonProps, IModalButtonState> {
  constructor(props: IModalButtonProps) {
    super(props);
    this.state = {
      show: false,
    };
  }

  public open = () => { this.setState({ show: true }); };
  public close = () => { this.setState({ show: false }); };

  public render() {
    return <React.Fragment>
      <Button onClick={this.open} size={this.props.size} color={this.props.color}>{this.props.text}</Button>
      <Modal show={this.state.show} onClose={this.close} {...this.props.modalProps}>
        {this.props.children}
      </Modal>
    </React.Fragment>;
  }
}
