import { StrictMode } from 'react'
import { useNavigate } from 'react-router-dom';
import './index.css'
// import './LandingPage.css'
const StartUpPage = () => {
   const background = "/img/farm.png"; // Correct path for assets in the public folder
   const navigate = useNavigate();
   const MyButton = () => {
	return (
	  <button className="bg-blue-500 text-white px-4 py-2 rounded">
		Click Me
	  </button>
	);
  };
	const InstructionsPage = () => {
    navigate('/instructions'); 
    };
	const FarmingPage = () => {
		navigate('./FarmPage');
	};
    return (
       <div
       style={{
           backgroundImage: `url(${background})`,
           backgroundSize: 'cover', // Ensures the image covers the entire container
           backgroundPosition: 'center', // Centers the image
           backgroundAttachment: 'fixed', // Keeps the background fixed during scrolling
           height: '100vh', // Full viewport height
           width: '100%', // Full width
           margin: 0, // Remove any default margin
           padding: 0, // Remove any default padding
           border: 'none', // Ensure no border is applied


           // Flexbox for centering content
           display: 'flex',
           justifyContent: 'center', // Centers horizontally
           alignItems: 'center', // Centers vertically
           flexDirection: 'column', // Stacks the h1 and button vertically
       }}
       >
       <h1 style={{ textAlign: 'center', fontSize: '4rem', color: "white"}}>AI Farming Simulator</h1>
       <div
       style={{
           display: 'flex',
           justifyContent: 'center',
           gap: '20px', // Add some space between buttons
       }}
       >
           <button button className="bg-blue-500 text-white px-4 py-2 rounded"	 style={{ fontSize: '3rem' }}onClick={FarmingPage}>Play</button>
           <button button className="bg-blue-500 text-white px-4 py-2 rounded" style={{ fontSize: '3rem' }}  onClick={InstructionsPage}>Instructions</button>
       </div>
       </div>
   );
 };
export default StartUpPage;