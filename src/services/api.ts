import axios from "axios";

const isMessageValid = (prompt: string) => {
  return prompt?.trim() !== "";
};

const addSystemMessage = async (
  message: string,
  useAgents: boolean = false,
  streamResponse: boolean = false,
) => {
  try {
    const response = await axios.post(`${import.meta.env.VITE_API_URL}/chat`, {
      message,
      useAgents,
      streamResponse,
    });

    if (response.status === 200) {
      return response.data;
    }
  } catch (e) {
    console.error(e);
  }
};

const addUserMessage = (prompt: string) => {
  return prompt;
};

export function useApi() {
  return {
    isMessageValid,
    addSystemMessage,
    addUserMessage,
  };
}
