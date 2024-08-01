import React, { useState } from 'react';

const SetupDialog = ({ show, onClose, formData, handleChange }) => {

    if (!show) {
        return null;
    }

    return (
        <div className="dialog-overlay">
            <div className="setup-dialog">
                <h2>Setup your personal assistant</h2>
                <form>
                    <div className="form-group">
                    <label htmlFor="name">Name</label>
                    <input
                        type="text"
                        id="name"
                        name="name"
                        value={formData.name}
                        onChange={handleChange}
                    />
                    </div>
                    <div className="form-group">
                        <label htmlFor="style">Style</label>
                        <select
                            id="style"
                            name="style"
                            value={formData.style}
                            onChange={handleChange}
                        >
                            <option value="">Select a style</option>
                            <option value="classic">Classic</option>
                            <option value="modern">Modern</option>
                            <option value="minimalist">Minimalist</option>
                            <option value="descriptive">Descriptive</option>
                            <option value="descriptive">Poetic</option>
                        </select>
                    </div>
                    <div className="form-group">
                        <label htmlFor="tone">Tone</label>
                        <select
                            id="tone"
                            name="tone"
                            value={formData.tone}
                            onChange={handleChange}
                        >
                            <option value="">Select a tone</option>
                            <option value="serious">Serious</option>
                            <option value="humorous">Humorous</option>
                            <option value="dark">Dark</option>
                            <option value="light-hearted">Light-hearted</option>
                            <option value="Suspenseful">Suspenseful</option>
                            <option value="extremly sarcastic">Extremly Sarcastic</option>
                        </select>
                    </div>
                    <div className="form-group">
                        <label htmlFor="reference">Reference</label>
                        <input
                            type="text"
                            id="reference"
                            name="reference"
                            value={formData.reference}
                            onChange={handleChange}
                        />
                    </div>
                    <button type="button" onClick={onClose}>Submit</button>
                </form>
            </div>
        </div>
    );
};

export default SetupDialog;
