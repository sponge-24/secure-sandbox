import { useState } from "react";
import axios from "axios";
import EditorPanel from "./EditorPanel";
import OutputPanel from "./OutputPanel";

const CodeEditor = () => {
  const [code, setCode] = useState('print("Hello, world!")');
  const [output, setOutput] = useState("");
  const [running, setRunning] = useState(false);

  const handleRun = async () => {
    setRunning(true);
    setOutput("Running...");

    try {
      const response = await axios.post("http://localhost:8000/run", { code });
      const jobId = response.data.job_id;

      const pollResult = async () => {
        const res = await axios.get(`http://localhost:8000/result/${jobId}`);
        if (res.data.status === "done") {
          setOutput(res.data.output);
          setRunning(false);
        } else {
          setTimeout(pollResult, 500);
        }
      };

      pollResult();
    } catch (err) {
      setOutput("Error: " + err.message);
      setRunning(false);
    }
  };

  return (
    <div className="flex h-screen font-mono bg-gray-950 text-gray-100">
      <EditorPanel
        code={code}
        setCode={setCode}
        handleRun={handleRun}
        running={running}
      />
      <OutputPanel output={output} />
    </div>
  );
};

export default CodeEditor;
