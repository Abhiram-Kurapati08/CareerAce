import React, { useState, useEffect } from "react";
import "./ResponsivePage.css";
import PreloaderGif from "../assets/preloader.gif";
import helloImage from "../assets/hello.png";
import thinkingImage from "../assets/thinking.png";
import ideaImage from "../assets/idea.png";
import helloAudio from "../assets/hello_audio.mp3";  // Import hello.mp3
import recommendedAudio from "../assets/recommend_audio.mp3";  // Import recommended.mp3

function ResponsivePage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isServing, setIsServing] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [characterImage, setCharacterImage] = useState(helloImage);
  const [waitingForRoadmapResponse, setWaitingForRoadmapResponse] = useState(false);

  useEffect(() => {
    const checkServer = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/check");
        const data = await response.json();
        if (data.status === "serving") {
          setIsServing(true);
          setMessages([{ sender: "bot", text: "Choose an option:\nA) Upload your resume for automatic extraction.\nB) Enter details manually." }]);
        }
      } catch (error) {
        console.error("Server is not responding:", error);
        setIsServing(false);
      }
    };

    // Play the hello.mp3 when the page is loaded
    const helloAudioElement = new Audio(helloAudio);
    helloAudioElement.play();

    checkServer();
  }, []);

  const sendMessage = async () => {
    const userMessage = { sender: "user", text: input.trim() };
    if (!input.trim()) return;

    setMessages([...messages, userMessage]);

    if (waitingForRoadmapResponse) {
      handleRoadmapResponse(input.trim());
      setInput(""); // Clear input field immediately after sending
      return;
    }

    setMessages((prevMessages) => [...prevMessages, { sender: "bot", text: "", isLoading: true }]);
    setIsLoading(true);
    setCharacterImage(thinkingImage);

    if (input.trim().toUpperCase() === "A") {
      setIsUploading(true);
      setMessages((prevMessages) => prevMessages.slice(0, -1));
      setMessages((prevMessages) => [...prevMessages, { sender: "bot", text: "Please upload your resume." }]);
      setIsLoading(false);
      setInput(""); // Clear input field immediately after sending
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input.trim() }),
      });
      const data = await response.json();

      setTimeout(() => {
        setMessages((prevMessages) => prevMessages.slice(0, -1));
        setMessages((prevMessages) => [
          ...prevMessages,
          userMessage,
          { sender: "bot", text: formatText(data.response) },
        ]);

        if (data.roadmap_option) {
          setMessages((prevMessages) => [
            ...prevMessages,
            { sender: "bot", text: "Would you like a detailed roadmap? (Yes/No)" },
          ]);
          setWaitingForRoadmapResponse(true);
        }

        setCharacterImage(ideaImage);
        setIsLoading(false);
        setInput(""); // Clear input field immediately after sending
      }, 1500);
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  const handleRoadmapResponse = (response) => {
    if (response.toLowerCase() === "yes") {
      // Play recommended.mp3 before calling generate_roadmap
      const recommendedAudioElement = new Audio(recommendedAudio);
      recommendedAudioElement.play();
      setMessages((prevMessages) => [...prevMessages, { sender: "bot", text: "Generating roadmap...", isLoading: true }]);
      generateRoadmap();
    } else {
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: "bot", text: "Alright! Let me know if you need further help." },
      ]);
    }
    setWaitingForRoadmapResponse(false);
  };

  const generateRoadmap = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/generate_roadmap", { method: "POST" });
      const data = await response.json();

      setTimeout(() => {
        setMessages((prevMessages) => prevMessages.slice(0, -1));
        setMessages((prevMessages) => [
          ...prevMessages,
          { sender: "bot", text: formatText(data.response) },
        ]);
      }, 1500);
    } catch (error) {
      console.error("Error generating roadmap:", error);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === "Enter" && !isLoading) {
      event.preventDefault();
      sendMessage();
    }
  };

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const uploadFile = async () => {
    if (!selectedFile) return;
    const formData = new FormData();
    formData.append("file", selectedFile);

    setMessages([...messages, { sender: "bot", text: "", isLoading: true }]);
    setIsLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();

      setMessages((prevMessages) => prevMessages.slice(0, -1));
      setMessages((prevMessages) => [...prevMessages, { sender: "bot", text: data.response }]);
      setIsUploading(false);
    } catch (error) {
      console.error("Error uploading file:", error);
    }

    setIsLoading(false);
  };

  const formatText = (text) => {
    const formattedText = text
      .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
      .replace(/### (\d+\.\d+ .+?):/g, '<i>$1</i>');

    const lines = formattedText.split("\n").map((line, index) => (
      <p key={index} dangerouslySetInnerHTML={{ __html: line }} />
    ));

    return lines;
  };

  return (
    <div className="chat-container-wrapper">
      <div className="chatbot">
        <header>
          <h2>CareerAce</h2>
        </header>
        <ul className="chatbox">
          {messages.map((msg, index) => (
            <li key={index} className={`chat ${msg.sender === "user" ? "outgoing" : "incoming"}`}>
              {msg.isLoading ? <img src={PreloaderGif} alt="Loading..." className="preloader" /> : <p>{msg.text}</p>}
            </li>
          ))}
        </ul>
        <div className="chat-input">
          {isUploading ? (
            <>
              <input type="file" accept=".pdf" onChange={handleFileChange} />
              <button onClick={uploadFile} disabled={!selectedFile}>Upload</button>
            </>
          ) : (
            <>
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyPress}
                placeholder="Enter a message..."
                spellCheck="false"
                required
                disabled={!isServing || isLoading}
              ></textarea>
              <span id="send-btn" className="send-button" onClick={sendMessage}>Send</span>
            </>
          )}
        </div>
      </div>

      <div className="character-wrapper">
        <img src={characterImage} alt="Character" className="character-image" />
      </div>
    </div>
  );
}

export default ResponsivePage;
