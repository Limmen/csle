import './Container.css';
import Header from "./Header/Header";
import Footer from "./Footer/Footer";
import Container from "./Container/Container";

function NavTest() {
  return (
      <div className="Container index container-fluid">
        <div className="row">
          <div className="col-sm-12">
              <Container/>
          </div>
        </div>
        <Footer/>
      </div>
  );
}

NavTest.propTypes = {};
NavTest.defaultProps = {};
export default NavTest;
