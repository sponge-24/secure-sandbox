const OutputPanel = ({ output }) => {
  return (
    <div className="w-1/2 flex flex-col p-4 bg-gray-950 text-gray-100">
      <h2 className="text-lg font-semibold mb-3 text-gray-300">Output</h2>
      <pre className="flex-1 bg-gray-900 p-4 rounded-lg border border-gray-800 overflow-auto whitespace-pre-wrap text-sm">
        {output}
      </pre>
    </div>
  );
};

export default OutputPanel;
