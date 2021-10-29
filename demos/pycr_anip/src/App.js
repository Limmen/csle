//import logo from './logo.svg';
import './App.css';
import Header from "./components/Header/Header";
import Footer from "./components/Footer/Footer";
import Main from "./components/Main/Main";

function App() {
  return (
      <div className="App index container-fluid">
        <Header></Header>
        <div className="row">
          <div className="col-sm-1"></div>
          <div className="col-sm-10">
            <Main/>
          </div>
          <div className="col-sm-1"></div>
        </div>
        <Footer/>
      </div>
  );
}

export default App;
