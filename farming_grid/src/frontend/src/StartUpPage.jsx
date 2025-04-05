import { StrictMode } from 'react'
import "./StartUpPage.css"
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
		margin: 0,          // Remove any default margin
    padding: 0,         // Remove any default padding
    border: 'none',     // Ensure no border is applied
		  
		}}
	  >
		<h1 style={{textAlign: 'center', fontSize : '4rem'}}>Welcome to My Page</h1>
	  </div>
	);
  };
export default StartUpPage;