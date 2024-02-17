import React from 'react';
import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Home from '../src/component/Home';
import UserProfile from '../src/component/UserProfile'

const AppRouter = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/user/:id" element={<UserProfile />} />
      </Routes>
    </Router>
  );
};

export default AppRouter;