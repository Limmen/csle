import './MainContainer.css';
import Header from "./Header/Header";
import {Outlet} from "react-router-dom";
import Footer from "./Footer/Footer";

/**
 * Container component containing the main components of the page
 */
const MainContainer = (props) => {
  return (
      <div className="Container index container-fluid">
        <Header sessionData={props.sessionData} setSessionData={props.setSessionData}></Header>
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
