import { useLocation, useNavigate } from "react-router-dom";
import { Tree } from "react-tree-graph"; // Use named import
import "react-tree-graph/dist/style.css"; // Import the default styles
import { useEffect, useState } from "react";

function FolderStructure() {
  const location = useLocation();
  const navigate = useNavigate();
  const folderData = location.state?.folderData;
  const [data, setData] = useState({});

  useEffect(() => {
    if (!folderData || typeof folderData !== "object") {
      console.error("No valid folder data available.");
      navigate("/");
    } else {
      const treeData = convertToTree(folderData.folder_structure);
      setData(treeData);
    }
  }, [folderData, navigate]);

  const convertToTree = (data) => {
    return {
      name: "root",
      children: Object.entries(data).map(([key, value]) => ({
        name: key,
        children: [
          ...(Array.isArray(value.folders)
            ? value.folders.map((folder) => ({ name: folder }))
            : []),
          ...(Array.isArray(value.files)
            ? value.files.map((file) => ({ name: file }))
            : []),
        ],
      })),
    };
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl mb-4">Folder Structure</h2>
      {data.children ? (
        <Tree
          data={data}
          height={3200}
          width={1200} // Increase width to give nodes more space
          animated // Enable animations for better visibility
          svgProps={{
            className: "custom-tree", // Custom class for styling
          }}
          nodeProps={{
            r: 8, // Adjust radius of the nodes if necessary
          }}
          textProps={{
            dy: 20, // Vertical adjustment
            dx: 15, // Move text horizontally to avoid overlap with lines
          }}
        />
      ) : (
        <p className="text-gray-600">No data available</p>
      )}
    </div>
  );
}

export default FolderStructure;
