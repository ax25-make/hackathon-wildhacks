import { StrictMode } from 'react'
import { useNavigate } from 'react-router-dom';

// import './LandingPage.css'
const Game = () => {
    const generateGrid = () => {
        const grid = [];
        for (let row = 0; row < 8; row++) {
            for (let col = 0; col < 8; col++) {
                grid.push(
                    <button
                        key={`${row}-${col}`}
                        style={{
                            fontSize: '1rem',
                            width: '60px',
                            height: '60px',
                            margin: '5px', 
                        }}
                    >
                        {`${row},${col}`}
                    </button>
                );
            }
        }
        return grid;
    };

    return (
        <div>
            <h1 style={{ textAlign: 'center', fontSize: '3rem' }}>Instructions</h1>
            <div
                style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(8, 1fr)', // Create 8 columns
                    gridGap: '10px', // Space between the buttons
                    justifyItems: 'center', // Center each button in the grid
                    marginTop: '20px', // Add margin at the top for spacing
                }}
            >
                {generateGrid()}
            </div>
        </div>
    );
 };
export default Game;