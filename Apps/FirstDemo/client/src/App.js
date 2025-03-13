import { useState } from "react";

function App() {
  const [prompt, setPrompt] = useState("");
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);

  const generateImage = async () => {
    setLoading(true);
    const res = await fetch(`http://127.0.0.1:8000/generate/?prompt=${prompt}`);
    const data = await res.json();
    
    if (data.image_path) {
      setImage(data.image_path);
    } else {
      alert("Error generating image: " + data.error);
    }
    
    setLoading(false);
  };

  return (
    <div style={{ textAlign: "center" }}>
      <h1>AI Art Generator</h1>
      <input
        type="text"
        placeholder="Enter your AI prompt..."
        onChange={(e) => setPrompt(e.target.value)}
        style={{ padding: "10px", width: "300px" }}
      />
      <button onClick={generateImage} disabled={loading} style={{ marginLeft: "10px", padding: "10px" }}>
        {loading ? "Generating..." : "Generate AI Art"}
      </button>
      <div>
        {image && <img src={image} alt="Generated AI Art" style={{ marginTop: "20px", maxWidth: "100%" }} />}
      </div>
    </div>
  );
}

export default App;

// import { useState } from "react";

// function App() {
//   const [prompt, setPrompt] = useState("");
//   const [image, setImage] = useState(null);

//   const generateImage = async () => {
//     const res = await fetch(`http://127.0.0.1:8000/generate/?prompt=${prompt}`);
//     const data = await res.json();
//     setImage(data.image_path);
//   };

//   return (
//     <div>
//       <input type="text" onChange={(e) => setPrompt(e.target.value)} />
//       <button onClick={generateImage}>Generate AI Art</button>
//       {image && <img src={image} alt="Generated Art" />}
//     </div>
//   );
// }

// export default App;

// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;
