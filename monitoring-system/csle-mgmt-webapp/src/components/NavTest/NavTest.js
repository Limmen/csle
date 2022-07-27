import './Container.css';
import Footer from "./Management/Footer/Footer";
import Management from "./Management/Container";
import Navbar from 'react-bootstrap/Navbar';

function NavTest() {
  return (
      <div className="Container index container-fluid">
        <div className="row">
          <div className="col-sm-12">
              <Navbar bg="light">
                  <BootstrapContainer>
                      <Navbar.Brand href="#home">Brand link</Navbar.Brand>
                  </BootstrapContainer>
              </Navbar>
              <Management/>
          </div>
        </div>
        <Footer/>
      </div>
  );
}

NavTest.propTypes = {};
NavTest.defaultProps = {};
export default NavTest;
