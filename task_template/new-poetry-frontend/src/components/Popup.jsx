import ReactDOM from 'react-dom';

const Popup = ({ content, onClose }) => {
  return ReactDOM.createPortal(
    <div className="popup-overlay">
      <div className="popup-content">
        <button className="close-button" onClick={onClose}>Close</button>
        <div dangerouslySetInnerHTML={{ __html: content }} />
      </div>
    </div>,
    document.getElementById('popup-root') // Assuming you have a div with id 'popup-root' in your HTML
  );
};

export default Popup;

