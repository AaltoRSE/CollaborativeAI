import { GRID_SIZE } from '../utils/constants'

const Inventory = ({ inventory }) => {
  const handleDragStart = (e, item) => {
    e.dataTransfer.setData("item", JSON.stringify(item));
  };

  return (
    <div className="inventory-container">
      <h3 className="inventory-title">Furnitures</h3>
      <div className="inventory-items">
        {inventory.map(item => {
          return (
            <div
              key={item.id}
              draggable={true}
              onDragStart={(e) => handleDragStart(e, item)}
              className="inventory-item"
              style={{
                width: `${item.width * GRID_SIZE}px`,
                height: `${item.height * GRID_SIZE}px`,
                backgroundColor: item.backgroundColor
              }}
            >
              {item.type}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Inventory;
