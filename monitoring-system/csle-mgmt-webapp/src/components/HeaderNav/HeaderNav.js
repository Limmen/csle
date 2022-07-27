import './HeaderNav.css';
import Footer from "./Management/Footer/Footer";
import Management from "./Management/Management";
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Logo from './logo.jpg'

function HeaderNav() {
  return (
      <div className="Container index container-fluid">
        <div className="row">
          <div className="col-sm-12">
              <Navbar bg="dark" variant="dark" expand="lg" className="csleNav">
                  <Container>
                      <Navbar.Brand href="#home">Cyber Security Learning Environment (CSLE)</Navbar.Brand>
                      <Navbar.Toggle aria-controls="basic-navbar-nav" />
                      <Navbar.Collapse id="basic-navbar-nav">
                          <Nav className="me-auto">
                              <Nav.Link href="#home">Login</Nav.Link>
                              <Nav.Link href="#link">About</Nav.Link>
                              <Nav.Link href="#link">Downloads</Nav.Link>
                              <NavDropdown title="Management System" id="basic-nav-dropdown">
                                  <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
                                  <NavDropdown.Item href="#action/3.2">
                                      Another action
                                  </NavDropdown.Item>
                                  <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
                                  <NavDropdown.Divider />
                                  <NavDropdown.Item href="#action/3.4">
                                      Separated link
                                  </NavDropdown.Item>
                              </NavDropdown>
                          </Nav>
                      </Navbar.Collapse>
                  </Container>
              </Navbar>
              <Management/>
          </div>
        </div>
        <Footer/>
      </div>
  );
}

HeaderNav.propTypes = {};
HeaderNav.defaultProps = {};
export default HeaderNav;
