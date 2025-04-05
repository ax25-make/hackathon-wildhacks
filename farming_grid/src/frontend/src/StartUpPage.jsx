import { StrictMode } from 'react'
// import './LandingPage.css'
const StartUpPage = () => {
   const background = "/img/13.jpg"; // Correct path for assets in the public folder
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
       <h1 style={{ textAlign: 'center', fontSize: '4rem' }}>AI Farming Simulator 🐶🐱🐭🐹</h1>
       <div
       style={{
           display: 'flex',
           justifyContent: 'center',
           gap: '20px', // Add some space between buttons
       }}
       >
           <button style={{ fontSize: '3rem' }}>Play</button>
           <button style={{ fontSize: '3rem' }}>Instructions</button>
       </div>
       </div>
   );
 };
export default StartUpPage;