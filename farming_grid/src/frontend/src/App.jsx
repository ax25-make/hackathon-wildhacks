import { BrowserRouter, Routes, Route } from "react-router-dom";
import StartUpPage from './StartUpPage.jsx';
import Instructions from './Instruction.jsx';


// Routes to navigate between pages - App holds all my routes and / is the default path
// So when I go to localhost:/ landing page is the first component that comes up 

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<StartUpPage/>}/>
		<Route path="/instructions" element = {<Instructions/>}/>
      </Routes>
    </BrowserRouter>
  );
}