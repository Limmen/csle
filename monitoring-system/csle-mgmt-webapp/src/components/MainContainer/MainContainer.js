import './MainContainer.css';
import Header from "./Header/Header";
import {Outlet} from "react-router-dom";
import Footer from "./Footer/Footer";

function MainContainer() {
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

MainContainer.propTypes = {};
MainContainer.defaultProps = {};
export default MainContainer;
