const EmotionFusionExplanation = () => {
    return (
        <div className="fusion-card">
            <h3>How Emotion Fusion Works</h3>

            <p>
                This system uses <strong>two sources</strong> to understand your emotional state:
            </p>

            <ul>
                <li>
                    📝 <strong>Text Emotion</strong> — detected from the words you type
                </li>
                <li>
                    🎥 <strong>Facial Emotion</strong> — detected from your facial expressions via camera
                </li>
            </ul>

            <p>
                These emotions are combined using a <strong>weighted fusion approach</strong>:
            </p>

            <ul>
                <li>Text Emotion Weight: <strong>60%</strong></li>
                <li>Facial Emotion Weight: <strong>40%</strong></li>
            </ul>

            <p>
                If both emotions agree, the confidence is higher.
                If they differ, the system selects the emotion with greater emotional priority.
            </p>

            <p className="note">
                ⚠️ No images or videos are stored. Facial analysis happens only in your browser.
            </p>
        </div>
    );
};

export default EmotionFusionExplanation;
