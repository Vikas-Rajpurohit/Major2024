import { useNavigate } from "react-router-dom";
import { useState } from "react";

function FormPage() {
  const [link, setLink] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const submitLink = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await fetch(
        "http://127.0.0.1:5000/get-folder-structure",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ repo_url: link }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to fetch folder structure. Please try again.");
      }

      const data = await response.json();
      navigate("/folder-structure", { state: { folderData: data } });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-lg p-6 bg-white shadow-md rounded-lg">
        <h2 className="text-lg font-semibold mb-4 text-center">
          Enter your GitHub Link
        </h2>

        {error && <p className="text-red-600 text-center mb-4">{error}</p>}

        <div className="flex items-center mb-4">
          <input
            type="text"
            placeholder="Enter link here"
            value={link}
            onChange={(e) => setLink(e.target.value)}
            className="flex-grow border-2 border-gray-300 p-2 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
            aria-label="GitHub link"
          />
          <button
            onClick={submitLink}
            className={`px-4 py-2 bg-indigo-600 text-white rounded-r-lg hover:bg-indigo-500 transition duration-200 ${
              loading ? "opacity-50 cursor-not-allowed" : ""
            }`}
            disabled={loading}
          >
            {loading ? "Loading..." : "Submit"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default FormPage;
