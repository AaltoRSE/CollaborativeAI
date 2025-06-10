import { GRID_SIZE } from '../utils/constants'

const FurnitureItem = ({ item, rotation = 0, onContextMenu }) => {
  const handleDragStart = (e) => {
    e.dataTransfer.setData("item", JSON.stringify(item));
  };

  const handleContextMenu = (e) => {
    if (onContextMenu) {
      onContextMenu(e, item.id);
    }
  };

  const isRotated = rotation % 180 !== 0;
  const boxWidth = (isRotated ? item.height : item.width) * GRID_SIZE;
  const boxHeight = (isRotated ? item.width : item.height) * GRID_SIZE;

  return (
    <div
      className="furniture"
      style={{
        backgroundColor: item.backgroundColor,
        width: `${boxWidth}px`,
        height: `${boxHeight}px`
      }}
      draggable={true}
      onDragStart={handleDragStart}
      onContextMenu={handleContextMenu}
    >
      {item.type}
    </div>
  );
};

export default FurnitureItem;
