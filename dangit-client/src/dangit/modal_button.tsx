import * as React from "react";
import { Button, Modal } from "react-bulma-components";
export { Modal } from "react-bulma-components";

export interface IModalButtonProps {
  size?: string;
  color?: string;
  renderAsLink?: boolean;
  text: string;
  className?: string;
  modalProps?: any;
  children: (modalComponent: ModalButton) => void;
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
      {this.props.renderAsLink || <Button onClick={this.open} size={this.props.size} color={this.props.color} className={this.props.className}>{this.props.text}</Button>}
      {this.props.renderAsLink && <a onClick={this.open} className={this.props.className}>{this.props.text}</a>}
      <Modal show={this.state.show} onClose={this.close} {...this.props.modalProps}>
        {this.props.children(this)}
      </Modal>
    </React.Fragment>;
  }
}
