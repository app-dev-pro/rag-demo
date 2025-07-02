"use client";

import { useState } from "react";

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [isQuerying, setIsQuerying] = useState(false);

  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setUploadStatus("Please select a file");
      return;
    }

    setIsUploading(true);
    setUploadStatus("Uploading and processing file...");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/api/ingest", {
        method: "POST",
        body: formData,
      });
      
      if (res.ok) {
        const data = await res.json();
        setUploadStatus(`✅ ${data.message}`);
        setFile(null);
        // Reset file input
        document.getElementById("fileInput").value = "";
      } else {
        setUploadStatus("❌ Upload failed");
      }
    } catch (error) {
      setUploadStatus("❌ Error uploading file");
      console.error("Upload error:", error);
    } finally {
      setIsUploading(false);
    }
  };

  const handlePromptSubmit = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) {
      return;
    }

    setIsQuerying(true);
    setResponse("Thinking...");

    try {
      const res = await fetch("http://localhost:8000/api/prompt", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt }),
      });
      
      if (res.ok) {
        const data = await res.json();
        setResponse(data.response);
      } else {
        setResponse("❌ Error getting response");
      }
    } catch (error) {
      setResponse("❌ Error connecting to backend");
      console.error("Query error:", error);
    } finally {
      setIsQuerying(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            RAG Demo
          </h1>
          <p className="text-lg text-gray-600">
            Upload documents and ask questions about them
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* File Upload Section */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              📄 Upload Document
            </h2>
            <form onSubmit={handleFileUpload} className="space-y-4">
              <div>
                <label
                  className="block text-sm font-medium text-gray-700 mb-2"
                  htmlFor="fileInput"
                >
                  Select a text file to upload
                </label>
                <input
                  id="fileInput"
                  type="file"
                  accept=".txt,.md,.doc,.docx"
                  onChange={(e) => setFile(e.target.files[0])}
                  className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                />
              </div>
              
              <button
                type="submit"
                disabled={!file || isUploading}
                className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-2 px-4 rounded-lg transition duration-200"
              >
                {isUploading ? "Processing..." : "Upload & Process"}
              </button>
              
              {uploadStatus && (
                <div className={`text-sm p-3 rounded ${
                  uploadStatus.includes("✅") 
                    ? "bg-green-100 text-green-700" 
                    : uploadStatus.includes("❌")
                    ? "bg-red-100 text-red-700"
                    : "bg-blue-100 text-blue-700"
                }`}>
                  {uploadStatus}
                </div>
              )}
            </form>
          </div>

          {/* Query Section */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              💬 Ask Questions
            </h2>
            <form onSubmit={handlePromptSubmit} className="space-y-4">
              <div>
                <label
                  className="block text-sm font-medium text-gray-700 mb-2"
                  htmlFor="prompt"
                >
                  What would you like to know?
                </label>
                <textarea
                  id="prompt"
                  rows="4"
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="Ask a question about your uploaded documents..."
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              
              <button
                type="submit"
                disabled={!prompt.trim() || isQuerying}
                className="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-semibold py-2 px-4 rounded-lg transition duration-200"
              >
                {isQuerying ? "Thinking..." : "Ask Question"}
              </button>
            </form>
          </div>
        </div>

        {/* Response Section */}
        {response && (
          <div className="mt-8 bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              🤖 Response
            </h2>
            <div className="bg-gray-50 p-4 rounded-lg">
              <p className="text-gray-800 whitespace-pre-wrap">{response}</p>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
