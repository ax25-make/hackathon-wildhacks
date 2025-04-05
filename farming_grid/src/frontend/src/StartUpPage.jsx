import { StrictMode } from 'react'
import "./StartUpPage.css"
// import './LandingPage.css'
const StartUpPage = () => {
	const background = "/img/13.jpg"; // Correct path for assets in the public folder
  
	return (
		<div style={{ backgroundImage: `url(${background})`,
		backgroundSize: 'cover', // Ensure the image covers the entire element
		backgroundPosition: 'center', // Center the image
		backgroundAttachment: 'fixed', // Optional: Keep the background fixed during scroll
		height: '100vh', // Make the element take up the full viewport height
		width: '100%', }}>
			<div>
				<h1 style={{textAlign: 'center', fontSize : '4rem'}}>Welcome to My Page</h1>


			</div>
	  </div>
	);
  };
export default StartUpPage;