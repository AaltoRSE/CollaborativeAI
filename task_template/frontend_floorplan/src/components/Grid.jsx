import { useState, useEffect } from 'react';
import FurnitureItem from './FurnitureItem';
import { GRID_SIZE } from '../utils/constants'

const Grid = ({ tileMap, items, onDropItem, onMoveItem, onDeleteItem }) => {
  const [hoveredTile, setHoveredTile] = useState(null);
  const [contextMenu, setContextMenu] = useState(null);

  useEffect(() => {
    window.addEventListener('click', () => setContextMenu(null));
    return () => window.removeEventListener('click', close);
  }, []);

  const handleDrop = async (e) => {
    const itemData = JSON.parse(e.dataTransfer.getData("item"));
    const rect = e.currentTarget.getBoundingClientRect();
    const x = Math.floor((e.clientX - rect.left) / GRID_SIZE) - itemData.grabOffsetX;
    const y = Math.floor((e.clientY - rect.top) / GRID_SIZE) - itemData.grabOffsetY;
    const isExisting = items.some(i => i.id === itemData.id);

    if (isExisting) {
      onMoveItem(itemData.id, x, y);
    } else {
      onDropItem(itemData, x, y);
    }
    setHoveredTile(null);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    const rect = e.currentTarget.getBoundingClientRect();
    const x = Math.floor((e.clientX - rect.left) / GRID_SIZE);
    const y = Math.floor((e.clientY - rect.top) / GRID_SIZE);
    setHoveredTile({ x, y });
  };

  const handleRotateItem = (id) => {
    onMoveItem(id, null, null, true);
  };

  return (
    <div
      className="grid"
      style={{
        width: tileMap[0].length * GRID_SIZE,
        height: tileMap.length * GRID_SIZE
      }}
      onDragOver={handleDragOver}
      onDrop={handleDrop}
    >

      {tileMap.map((row, y) =>
        row.map((cell, x) => {
          let backgroundColor = "transparent";
          if (cell === 1) 
            backgroundColor = '#f0f0f0';
          else if (cell === 3) 
            backgroundColor = 'lightblue';
          else if (cell === 4) 
            backgroundColor = 'brown';
          else if (cell === 0) 
            backgroundColor = '#aaa';

          return (
            <div
              key={`${x}-${y}`}
              className="tile"
              style={{
                left: x * GRID_SIZE,
                top: y * GRID_SIZE,
                backgroundColor,
              }}
            />
          );
        })
      )}

      {hoveredTile && (
        <div
          style={{
            left: hoveredTile.x * GRID_SIZE,
            top: hoveredTile.y * GRID_SIZE,
            width: GRID_SIZE,
            height: GRID_SIZE,
            border: '2px dashed',
            position: 'absolute',
          }}
        />
      )}

      {items.map(item => (
        <div
          key={item.id}
          style={{
            position: 'absolute',
            left: item.x * GRID_SIZE,
            top: item.y * GRID_SIZE
          }}
        >
          <FurnitureItem
            item={item}
            rotation={item.rotation}
            onContextMenu={(e, id) => {
              e.preventDefault();
              setContextMenu({ x: e.clientX, y: e.clientY, itemId: id });
            }}
          />
        </div>
      ))}

      {contextMenu && (
        <div
          className="context-menu"
          style={{
            position: 'fixed',
            top: contextMenu.y,
            left: contextMenu.x,
            backgroundColor: '#fff',
            border: '1px solid #ccc',
            boxShadow: '0 2px 5px rgba(0,0,0,0.2)',
            padding: '6px',
            borderRadius: '6px',
          }}
        >
          <div
            style={{ padding: '4px 8px', cursor: 'pointer' }}
            onClick={() => {
              handleRotateItem(contextMenu.itemId);
              setContextMenu(null);
            }}
          >
            Rotate
          </div>
          <div
            style={{ padding: '4px 8px', cursor: 'pointer', color: 'red' }}
            onClick={() => {
              onDeleteItem(contextMenu.itemId);
              setContextMenu(null);
            }}
          >
            Delete
          </div>
        </div>
      )}
    </div>
  );
};

export default Grid;
