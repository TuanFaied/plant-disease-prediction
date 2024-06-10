import React, { useState } from "react";

export default function ImageUpload() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [imageName, setImageName] = useState(""); // State to store image name
  const [predictionResult, setPredictionResult] = useState(null);
  const [isDragging, setIsDragging] = useState(false); // State to manage drag-over effect

  // Handle file selection and update the state
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedImage(URL.createObjectURL(file));
      setImageName(file.name); // Store the file name
    }
  };

  // Handle file drop and update the state
  const handleDrop = (event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    if (file) {
      setSelectedImage(URL.createObjectURL(file));
      setImageName(file.name); // Store the file name
    }
    setIsDragging(false);
  };

  // Prevent default behavior and show drag-over effect
  const handleDragOver = (event) => {
    event.preventDefault();
    setIsDragging(true);
  };

  // Remove drag-over effect when drag leaves
  const handleDragLeave = () => {
    setIsDragging(false);
  };

  // Simulate a disease prediction and show the result
  const handlePredict = () => {
    // Simulated result
    const simulatedResult = {
      disease: "Powdery Mildew",
      accuracy: "92%"
    };

    // Set the simulated prediction result
    setPredictionResult(simulatedResult);
  };

  return (
    <div className="flex justify-center items-center h-screen bg-cover bg-center bg-no-repeat bg-[url('https://png.pngtree.com/thumb_back/fw800/background/20231103/pngtree-stunning-close-up-shot-of-vibrant-green-leaves-in-a-natural-image_13748523.png')]">
      <div className="box-border h-6/7 w-1/2 p-4 rounded-2xl bg-black bg-opacity-50 border-green-500">
        <h1 className="text-4xl italic font-bold text-white">Leaf Disease Prediction</h1>

        <label
          className="block mb-2 text-sm font-medium text-white dark:text-white mt-4"
          htmlFor="multiple_files"
        >
          Upload Leaf Image for Prediction
        </label>

        <div className="relative">
          <input
            className="block w-full text-sm text-gray-900 border border-green-500 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-green-700 dark:border-green-600 dark:placeholder-gray-400"
            id="multiple_files"
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            title={imageName} // Show image name in tooltip
          />
          
        </div>

        <div className="grid-rows-2 mt-4">
          {!selectedImage ? (
            <div
              className={`flex flex-col items-center justify-center w-full h-64 border-2 border-dashed rounded-lg cursor-pointer bg-gray-50 ${
                isDragging ? "border-green-500" : "border-gray-300"
              }`}
              onDragOver={handleDragOver}
              onDrop={handleDrop}
              onDragLeave={handleDragLeave}
            >
              <div className="flex flex-col items-center justify-center pt-5 pb-6">
              <svg
                  className="w-8 h-8 mb-4 text-gray-500 dark:text-gray-400"
                  aria-hidden="true"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 20 16"
                >
                  <path
                    stroke="currentColor"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"
                  />
                </svg>

                <p className="mb-2 text-sm text-gray-500 dark:text-gray-400">
                  <span className="font-semibold">Drag and drop</span> 
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  SVG, PNG, JPG or GIF (MAX. 800x400px)
                </p>
              </div>
            </div>
          ) : (
            <div className="flex flex-col items-center w-full">
              <img
                src={selectedImage}
                alt="Preview"
                className="h-64 w-full object-contain rounded-lg"
              />
              <div className="text-sm text-white dark:text-gray-400 mt-2"> 
                {imageName}
              </div>
            </div>
          )}

          <div className="mt-4 row-start-2 flex flex-col items-center">
            <button
              type="button"
              onClick={handlePredict}
              className="text-white bg-gradient-to-r from-green-400 via-green-500 to-green-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-green-300 dark:focus:ring-green-800 shadow-lg shadow-green-500/50 dark:shadow-lg dark:shadow-green-800/80 font-medium rounded-lg text-sm px-5 py-2.5 text-center mb-2"
            >
              Predict Leaf Disease
            </button>

            {predictionResult && (
              <div className="mt-4 bg-gray-800 p-4 rounded-lg text-white w-full text-center">
                <p><strong>Disease Name:</strong> {predictionResult.disease}</p>
                <p><strong>Prediction Accuracy:</strong> {predictionResult.accuracy}</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
