
const FinishButton = ({ messages, isFinishClicked,isRatingSubmitted, toggleFinish }) => {
  return (
    <div className="finish-btn-wrapper">
        <button type="submit" className="finish-btn"
          disabled={isRatingSubmitted || messages.length <= 0}
          style={{
            "backgroundColor": isFinishClicked ? "#f44336" : "#6eb4ff",
            "cursor": isFinishClicked || messages.length <= 0 ? "not-allowed" : "pointer"
          }}
          onClick={toggleFinish}> 
          {isFinishClicked ? "Cancel" : "Finish"}
        </button>
    </div>
  );
}

export default FinishButton;