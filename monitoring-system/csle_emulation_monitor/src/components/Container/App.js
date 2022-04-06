//import logo from './logo.svg';
import './App.css';
import Header from "./components/Header/Header";
import Footer from "./components/Footer/Footer";
import Main from "./components/Main/Main";
import {Outlet} from "react-router-dom";

function App() {
  return (
      <div className="App index container-fluid">
        <Header></Header>
        <div className="row">
          <div className="col-sm-1"></div>
          <div className="col-sm-10">
              <Outlet/>
          </div>
          <div className="col-sm-1"></div>
        </div>
        <Footer/>
      </div>
  );
}

App.propTypes = {};
App.defaultProps = {};
export default App;
