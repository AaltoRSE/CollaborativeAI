import { useState } from 'react';
import Grid from './Grid';
import Inventory from './Inventory';
import taskService from '../services/task'
import html2canvas from 'html2canvas';
import { TILE_MAP, INVENTORY } from '../utils/constants'

const FloorplanGame = ({ messages, addMessage, setIsLoading, setIsDisabled }) => {
  const [inventory, setInventory] = useState(INVENTORY);

  const [furniture, setFurniture] = useState([]);

  function parsePoetryAndComment(input) {
    // Initialize variables to store the parsed parts
    let floor = "";
    let comment = "";
  
    // Trim the input to remove leading/trailing whitespace
    input = input.trim();
  
    // Check if the input starts with a '[' character
    if (input.startsWith('[')) {
        // Find the closing ']' character
        let endBracketIndex = input.indexOf(']');
        
        // If a closing ']' is found, extract the poetry line
        if (endBracketIndex !== -1) {
            floor = input.substring(1, endBracketIndex).trim();
            // Extract the comment part if there is any text after the closing ']'
            if (endBracketIndex + 1 < input.length) {
                comment = input.substring(endBracketIndex + 1).trim();
            }
        }
    } else {
        // If the input doesn't start with '[', consider the whole input as a comment
        comment = input;
    }
  
    // console.log("Parsed: ", floor, ", ", comment)
  
    return { floor, comment };
  }
  
  function checkAndAddMessage(sender, text, comment, type) {
    text = (typeof text === 'string' && text.trim()) ? text : null;
    comment = (typeof comment === 'string' && comment.trim()) ? comment : null;
  
    if (text === null && comment === null) {
      console.log("no message");
    } else {
      addMessage({ sender: sender, text: text, comment: comment, type: "dialogue"}); 
    }
  }

  const sendMove = async () => {
    setIsLoading(true);
    setIsDisabled(true);

    const floorPlanElement = document.getElementsByClassName("game")[0];
    const snapShot = await html2canvas(floorPlanElement);
    const floorPlanImage = snapShot.toDataURL()
    
    try {
      taskService
        .submitUserInput({
          inputData: {
            floorplans: messages
          }, 
          text: "", 
          image: floorPlanImage,
          objective: "bedroom"
        })
        .then((returnedResponse) => {
          console.log(returnedResponse)
          let parsed = parsePoetryAndComment(returnedResponse.text)
          checkAndAddMessage("ai", parsed.floor, parsed.comment, "dialogue")
          setIsLoading(false)
        })
        .catch((error) => {
          if (error.response && error.response.status === 429) {
            alert(error.response.data.error);
          } else {
            console.log(error);
          }
          setIsLoading(false)
          setIsDisabled(false)
        });
    } catch (err) {
      console.error('Failed to send user move or get AI response:', err);
    }
  }

  const handleDropItem = (item, x, y) => {
    const rotation = 0;
    const { width, height } = item;
    if (!canPlace(x, y, width, height)) return;

    setFurniture([...furniture, { ...item, x, y, rotation }]);
    setInventory(prev => prev.filter(i => i.id !== item.id));
    sendMove();
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
  
        sendMove();

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
      /> 
    </div>
  );
};

export default FloorplanGame;
