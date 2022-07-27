import './Container.css';
import Header from "./Header/Header";
import Footer from "./Footer/Footer";
import {Outlet} from "react-router-dom";

function Container() {
  return (
      <div className="Container index container-fluid">
        <Header></Header>
        <div className="row">
          <div className="col-sm-12">
              <Outlet/>
          </div>
        </div>
        <Footer/>
      </div>
  );
}

Container.propTypes = {};
Container.defaultProps = {};
export default Container;
