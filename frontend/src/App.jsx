import {
  BrowserRouter as Router,
  Route,
  Routes,
  useNavigate,
} from "react-router-dom";
import FormPage from "./pages/FormPage";
import FolderStructure from "./pages/FolderStructure";
import RagChat from "./pages/RagChat";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<FormPage />} />
        <Route path="/folder-structure" element={<FolderStructure />} />
        <Route path="/rag-chat" element={<RagChat />} />
      </Routes>
    </Router>
  );
}

export default App;
