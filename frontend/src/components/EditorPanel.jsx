import Editor from "@monaco-editor/react";

const EditorPanel = ({ code, setCode, handleRun, running }) => {
  return (
    <div className="w-1/2 flex flex-col border-r border-gray-800 bg-gray-900">
      <div className="flex-1">
        <Editor
          height="100%"
          defaultLanguage="python"
          value={code}
          onChange={(value) => setCode(value)}
          theme="vs-dark"
          options={{
            fontFamily: "Fira Code, monospace",
            fontSize: 14,
            minimap: { enabled: false },
            smoothScrolling: true,
          }}
        />
      </div>
      <button
        onClick={handleRun}
        disabled={running}
        className={`m-3 p-3 rounded-lg font-medium transition-colors ${
          running
            ? "bg-gray-700 text-gray-400 cursor-not-allowed"
            : "bg-blue-600 hover:bg-blue-700 text-white shadow"
        }`}
      >
        {running ? "Running..." : "▶ Run Code"}
      </button>
    </div>
  );
};

export default EditorPanel;
