import { BrowserRouter, Routes, Route } from "react-router-dom";
import StartUpPage from './StartUpPage.jsx';
import Instructions from './Instruction.jsx';
<<<<<<< HEAD
import PlayGame from './PlayGame.jsx';
=======
import FarmPage from './FarmPage.jsx';
>>>>>>> c19f227dd9596e9a563e2620729e0af61cd1c01a


// Routes to navigate between pages - App holds all my routes and / is the default path
// So when I go to localhost:/ landing page is the first component that comes up 

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<StartUpPage/>}/>
		<Route path="/instructions" element = {<Instructions/>}/>
<<<<<<< HEAD
    <Route path="/game" element={<PlayGame/>}/>
=======
		<Route path = "/FarmPage" element = {<FarmPage/>}/>
>>>>>>> c19f227dd9596e9a563e2620729e0af61cd1c01a
      </Routes>
    </BrowserRouter>
  );
}