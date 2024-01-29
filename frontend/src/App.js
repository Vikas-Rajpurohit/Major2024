import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import History from './pages/History';
import Product from './pages/Product';

function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <nav className="bg-gray-800">
          {/* Navigation bar */}
        </nav>
        <div className="flex-grow">
          <Routes>
            <Route exact path="/" element={Dashboard()} />
            <Route path="/products" element={Product()} />
            <Route path="/history" element={History()} />
          </Routes>
        </div>
        <footer className="bg-gray-800">
          {/* Footer */}
        </footer>
      </div>
    </Router>
  );
}

export default App;
