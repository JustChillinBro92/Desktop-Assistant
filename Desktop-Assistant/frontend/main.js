import { app, BrowserWindow } from "electron";
import { spawn } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

let mainWindow = null;
let backendProcess = null;

function startBackend() {
  const projectRoot = path.join(__dirname, "..");

  backendProcess = spawn("py", [
    "-m",
    "uvicorn",
    "backend.server:app",
    "--port",
    "8000",
  ], {
    cwd: projectRoot,
  });

  backendProcess.stdout.on("data", (data) => {
    console.log(`${data}`);
  });

  backendProcess.stderr.on("data", (data) => {
    console.error(`${data}`);
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1100,
    height: 700,
    show: true,
  });

  mainWindow.loadURL("http://localhost:5173");
}

app.whenReady().then(() => {
  startBackend();
  createWindow();
});

app.on("window-all-closed", () => {
  if (backendProcess) {
    backendProcess.kill();
  }

  if (process.platform !== "darwin") {
    app.quit();
  }
});