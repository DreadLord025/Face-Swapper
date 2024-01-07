import React, { useState } from "react";
import axios from "axios"; // Импорт axios
import "./App.css";

function App() {
  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);
  const [image1, setImage1] = useState(null);
  const [image2, setImage2] = useState(null);
  const [result1, setResult1] = useState(null);
  const [result2, setResult2] = useState(null);

  const handleImageUpload = (event, setImage, setFile) => {
    setFile(event.target.files[0]);
    setImage(URL.createObjectURL(event.target.files[0]));
  };

  const handleFaceSwap = async () => {
    console.log("file1 - ", file1);
    console.log("file2 - ", file2);

    // Создание объекта FormData и добавление изображений
    const formData = new FormData();
    formData.append("images", file1);
    formData.append("images", file2);

    // Отправка POST-запроса на сервер
    await axios
      .post("http://localhost:5000/upload", formData)
      .then((response) => {
        // Конвертация base64 в blob
        const blob1 = base64ToBlob(response.data.img1, "image/jpeg");
        const blob2 = base64ToBlob(response.data.img2, "image/jpeg");

        // Отображение blob в элементах img
        setResult1(URL.createObjectURL(blob1));
        setResult2(URL.createObjectURL(blob2));
      });
  };

  // Функция для конвертации base64 в blob
  const base64ToBlob = (base64, type) => {
    const byteCharacters = atob(base64);
    const byteArrays = [];

    for (let i = 0; i < byteCharacters.length; i++) {
      byteArrays.push(byteCharacters.charCodeAt(i));
    }

    return new Blob([new Uint8Array(byteArrays)], { type });
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Face Swapper</h1>
      </header>
      <main>
        <div className="image-upload">
          <h2>Загрузите изображения</h2>
          <div className="MainblockUpload">
            <div className="blockUpload">
              <input
                id="file"
                type="file"
                accept="image/*"
                onChange={(event) =>
                  handleImageUpload(event, setImage1, setFile1)
                }
              />
              <label for="file">Выберите файл</label>
              {image1 && (
                <img
                  style={{ paddingTop: "10px" }}
                  className="uploadImage"
                  src={image1}
                  alt="Preview"
                />
              )}
            </div>
            <div className="blockUpload">
              <input
                id="file2"
                type="file"
                accept="image/*"
                onChange={(event) =>
                  handleImageUpload(event, setImage2, setFile2)
                }
              />
              <label for="file2">Выберите файл</label>
              {image2 && (
                <img
                  style={{ paddingTop: "10px" }}
                  className="uploadImage"
                  src={image2}
                  alt="Preview"
                />
              )}
            </div>
          </div>
        </div>
        <div className="result">
          <h2>Результат</h2>
          <button className="buttonSwap" onClick={handleFaceSwap}>
            Face Swap
          </button>
          <div className="MainblockResult">
            <div className="blockUpload">
              {result1 && (
                <img
                  style={{ paddingTop: "10px" }}
                  className="resultImage"
                  src={result1}
                  alt="Result"
                />
              )}
            </div>
            <div className="blockUpload">
              {result2 && (
                <img
                  style={{ paddingTop: "10px" }}
                  className="resultImage"
                  src={result2}
                  alt="Result"
                />
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
