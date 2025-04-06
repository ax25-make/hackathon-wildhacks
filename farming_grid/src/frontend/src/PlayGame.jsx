import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './GamePage.css';

const API_URL = 'http://127.0.0.1:5000';

const GamePage = () => {
  const [gameState, setGameState] = useState(null);
  const [selectedAction, setSelectedAction] = useState(null);
  const [selectedCell, setSelectedCell] = useState(null);
  const [message, setMessage] = useState('');
  const [checkResult, setCheckResult] = useState('');

  useEffect(() => {
    fetchGameState();
  }, []);

  const fetchGameState = async () => {
    try {
      const response = await axios.get(`${API_URL}/state`);
      setGameState(response.data);
    } catch (error) {
      console.error('Error fetching game state:', error);
      setMessage('Error loading game state.');
    }
  };

  const handleActionSelect = (action) => {
    setSelectedAction(action);
    setSelectedCell(null);
    setCheckResult(''); // Clear previous check result
    setMessage(`Selected action: ${action}. Click on a grid cell.`);
  };

  const handleCellClick = (row, col) => {
    if (selectedAction && gameState) {
      setSelectedCell({ row, col });
      performAction(selectedAction, row, col);
    } else if (!selectedAction) {
      setMessage('Please select an action first.');
    }
  };

  const performAction = async (action, row, col) => {
    try {
      let data = { action, x: col, y: row };
      if (action === 'plant') {
        const plantType = prompt('Enter plant type:');
        if (!plantType) return;
        data = { ...data, plant_type: plantType };
      } else if (action === 'check') {
        const response = await axios.post(`${API_URL}/action`, data);
        setMessage(response.data.message || '');
        setCheckResult(response.data.status || 'No plant at this location.'); // Update check result
        setSelectedAction(null);
        setSelectedCell(null);
        return; // Exit early as we don't need to refetch the whole state immediately
      }
      const response = await axios.post(`${API_URL}/action`, data);
      setMessage(response.data.message || '');
      fetchGameState();
      setSelectedAction(null);
      setSelectedCell(null);
    } catch (error) {
      console.error(`Error performing ${action}:`, error);
      setMessage(error.response?.data?.error || `Error performing ${action}`);
    }
  };

  const handleAdvanceDay = async () => {
    try {
      const response = await axios.post(`${API_URL}/advance`);
      setMessage(response.data.message || '');
      fetchGameState();
    } catch (error) {
      console.error('Error advancing day:', error);
      setMessage(error.response?.data?.error || 'Error advancing day.');
    }
  };

  const handleBuySeed = async () => {
    const plantType = prompt('Enter plant type to buy:');
    const quantity = parseInt(prompt('Enter quantity to buy:'));
    if (plantType && !isNaN(quantity) && quantity > 0) {
      try {
        const response = await axios.post(`${API_URL}/buy`, { plant_type: plantType, quantity });
        setMessage(response.data.message || '');
        fetchGameState();
      } catch (error) {
        console.error('Error buying seed:', error);
        setMessage(error.response?.data?.error || 'Error buying seed.');
      }
    } else {
      setMessage('Invalid plant type or quantity.');
    }
  };

  const handleSellCrop = async () => {
    const plantType = prompt('Enter plant type to sell:');
    const quantity = parseInt(prompt('Enter quantity to sell:'));
    if (plantType && !isNaN(quantity) && quantity > 0) {
      try {
        const response = await axios.post(`${API_URL}/sell`, { plant_type: plantType, quantity });
        setMessage(response.data.message || '');
        fetchGameState();
      } catch (error) {
        console.error('Error selling crop:', error);
        setMessage(error.response?.data?.error || 'Error selling crop.');
      }
    } else {
      setMessage('Invalid plant type or quantity.');
    }
  };

  const handleHarvest = async () => {
    try {
      const response = await axios.post(`${API_URL}/action`, { action: 'harvest' });
      setMessage(response.data.message || '');
      fetchGameState();
    } catch (error) {
      console.error('Error harvesting:', error);
      setMessage(error.response?.data?.error || 'Error harvesting.');
    }
  };

  return (
    <div className="game-container">
      <h1>Farm Game</h1>
      {gameState ? (
        <div className="game-info">
          <p>Money: ${gameState.money ? gameState.money.toFixed(2) : 0}</p>
          <p>Day: {gameState.day}</p>
          <p>Season: {gameState.season}</p>
          <p>Remaining Turns: {gameState.remaining_turns}</p>
          <p>Market Prices: {JSON.stringify(gameState.market_prices)}</p>
          <p>Stock: {JSON.stringify(gameState.stock)}</p>
          <p>Seeds: {JSON.stringify(gameState.seeds)}</p>
        </div>
      ) : (
        <p>Loading game state...</p>
      )}

      <div className="actions">
        <h2>Actions</h2>
        <button onClick={() => handleActionSelect('plant')}>Plant</button>
        <button onClick={() => handleActionSelect('water')}>Water</button>
        <button onClick={() => handleActionSelect('fertilize')}>Fertilize</button>
        <button onClick={() => handleActionSelect('check')}>Check</button>
        <button onClick={handleHarvest}>Harvest All</button>
        <button onClick={handleBuySeed}>Buy Seed</button>
        <button onClick={handleSellCrop}>Sell Crop</button>
        <button onClick={handleAdvanceDay}>Advance Day</button>
      </div>

      {checkResult && <div className="check-result">Status: {checkResult}</div>}

      {gameState && (
        <div className="grid-container">
          {gameState.grid.map((row, rowIndex) => (
            <div key={rowIndex} className="grid-row">
              {row.map((cell, colIndex) => (
                <div
                  key={colIndex}
                  className={`grid-cell ${cell && cell.plant ? 'planted' : ''} ${selectedCell && selectedCell.row === rowIndex && selectedCell.col === colIndex ? 'selected' : ''}`}
                  onClick={() => handleCellClick(rowIndex, colIndex)}
                >
                  {cell && cell.plant ? (
                    <span className="plant-letter">{cell.plant.name.charAt(0).toUpperCase()}</span>
                  ) : null}
                  {selectedCell && selectedCell.row === rowIndex && selectedCell.col === colIndex && selectedAction && <div className="overlay">{selectedAction}</div>}
                </div>
              ))}
            </div>
          ))}
        </div>
      )}

      {message && <p className="message">{message}</p>}
    </div>
  );
};

export default GamePage;