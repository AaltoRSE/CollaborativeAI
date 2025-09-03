import { useState } from 'react';

const DialogueItem = ({ idx, message, handleEditMessage, style }) => {
  const messageClass = message.sender === "user" ? "user-dialogue" : "ai-dialogue";

  return (
    <>
      {/* {isEditing ? (
        <form onSubmit={handleSubmit} className="edit-form">
          <textarea
            value={editedMessage}
            onChange={(event) => setEditedMessage(event.target.value)}
          />
          <button type="submit" disabled={!editedMessage.trim()}> Save </button>
        </form>
      ) : (
        <div className={`${style} ${messageClass}`} style={{cursor: "alias"}} onClick={handleEditClick}>
          {message.text} <br/> 
        </div>
      )} */}
      <div className={`${style} ${messageClass}`}>
          {message.text} <br/> 
      </div>
    </>
  );
};

export default DialogueItem;
