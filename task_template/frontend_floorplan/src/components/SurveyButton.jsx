const SurveyButton = ({ }) => {
  return (
    <button
      onClick={() => window.open("https://forms.gle/sBRPdCPEBwtWB6bw7", "_blank")}
      className="survey-button"
    >
      Feedback survey
    </button>
  );
};

export default SurveyButton;
