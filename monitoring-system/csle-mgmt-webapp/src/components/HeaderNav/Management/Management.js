import './Management.css';
import Header from "./Header/Header";
import {Outlet} from "react-router-dom";

function Management() {
  return (
      <div className="Container index container-fluid">
        <Header></Header>
        <div className="row">
          <div className="col-sm-12">
              <Outlet/>
          </div>
        </div>
      </div>
  );
}

Management.propTypes = {};
Management.defaultProps = {};
export default Management;
