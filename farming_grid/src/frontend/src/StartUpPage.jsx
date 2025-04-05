import { StrictMode } from 'react'
import "./StartUpPage.css"
// import './LandingPage.css'
const StartUpPage = () => {
	const background = "/img/13.jpg"; // Correct path for assets in the public folder
  
	return (
	  <div
		style={{
		  backgroundImage: `url(${background})`,
		  backgroundSize: 'auto',
		  height: '100vh'
		  
		}}
	  >
		<h1>Welcome to My Page</h1>
	  </div>
	);
  };
export default StartUpPage;