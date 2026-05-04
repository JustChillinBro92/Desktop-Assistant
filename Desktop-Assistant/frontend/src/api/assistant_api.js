const backend_url = "http://localhost:8000";
// const backend_url = "http://192.168.95.1:8000";

// send user message to backend AI
const sendMessage = async (message) => {
  const res = await fetch(`${backend_url}/text`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });

  // return AI response
  return res.json();
};

export { sendMessage };
