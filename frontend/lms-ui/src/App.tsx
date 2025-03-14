import React from "react";
import { Route, Routes, BrowserRouter } from "react-router-dom";
import MainWrapper from "./Layouts/MainWrapper";
import PrivateRoute from "./Layouts/PrivateRoute";
import Register from "./views/auth/Register";
import Login from "./views/auth/Login";
import Logout from "./views/auth/Logout";


const App: React.FC = () => {
    return (
        <BrowserRouter>
            <MainWrapper>
                <Routes>
                    <Route path="/register/" element={ <Register/>} /> 
                    <Route path="/login/" element={ <Login/>} /> 
                    <Route path="/logout/" element={ <Logout/>} /> 
                </Routes>
            </MainWrapper>
        </BrowserRouter>
  
  );
};

export default App;
