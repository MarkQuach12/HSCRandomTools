import "./App.css";
import Predict from "./components/pages/Predict";
import Band6 from "./components/pages/band6";
import Navbar from "./components/pages/Navbar";
import { Routes, Route } from "react-router-dom";
import Home from "./components/pages/Home";
import { Analytics } from "@vercel/analytics/react"
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function App() {
  return (
    <div className="pt-20 px-4">
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />}/>
        <Route path="/predict" element={<Predict />} />
        <Route path="/band6" element={<Band6 />} />
      </Routes>
      <Analytics />
      <ToastContainer
        pauseOnFocusLoss={false}
      />
    </div>
  );
}

export default App;
