import { useState } from 'react';
import Grid from './Grid';
import Inventory from './Inventory';
import { TILE_MAP, INVENTORY } from '../utils/constants'

const FloorplanGame = ({ messages, addMessage, setIsLoading, setIsDisabled }) => {
  const [inventory, setInventory] = useState(INVENTORY);

  const [furniture, setFurniture] = useState([]);

  const handleDropItem = (item, x, y) => {
    const rotation = 0;
    const { width, height } = item;
    if (!canPlace(x, y, width, height)) return;

    setFurniture([...furniture, { ...item, x, y, rotation }]);
    setInventory(prev => prev.filter(i => i.id !== item.id));
  };

  const handleMoveItem = (id, x, y, rotate = false) => {
    setFurniture(prev =>
      prev.map(item => {
        if (item.id !== id) return item;

        const newRotation = rotate ? (item.rotation + 90) % 360 : item.rotation;
        const rotatedSize = newRotation % 180 === 90
          ? { width: item.height, height: item.width }
          : { width: item.width, height: item.height }

        const newX = x !== null ? x : item.x;
        const newY = y !== null ? y : item.y;

        if (!canPlace(newX, newY, rotatedSize.width, rotatedSize.height)) return item;

        const movedItem = {
          ...item,
          x: newX,
          y: newY,
          rotation: newRotation
        };

        return movedItem;
      })
    );
  };

  const handleDeleteItem = (id) => {
    setFurniture(prevFurniture => {
      const itemToRemove = prevFurniture.find(item => item.id === id);
      if (!itemToRemove) return prevFurniture;
  
      setInventory(prevInventory => {
        if (!prevInventory.find(item => item.id === itemToRemove.id)) {
          return [...prevInventory, itemToRemove];
        }
        return prevInventory;
      });
  
      return prevFurniture.filter(item => item.id !== id);
    });
  };

  const canPlace = (x, y, w, h) => {
    for (let dx = 0; dx < w; dx++) {
      for (let dy = 0; dy < h; dy++) {
        const row = TILE_MAP[y + dy];
        if (!row || row[x + dx] !== 1) return false;
      }
    }
    return true;
  };

  return (
    <div className="game">
      <Inventory inventory={inventory} />
      <Grid
        tileMap={TILE_MAP}
        items={furniture}
        onDropItem={handleDropItem}
        onMoveItem={handleMoveItem}
        onDeleteItem={handleDeleteItem}
        messages={messages}
        addMessage={addMessage}
        setIsLoading={setIsLoading}
        setIsDisabled={setIsDisabled}
      /> 
    </div>
  );
};

export default FloorplanGame;
