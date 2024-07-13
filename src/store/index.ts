import { defineStore } from "pinia";
import { Message } from "../types";

export const useMessagesStore = defineStore("messages", {
  state: () => {
    return { messages: <Message[]>[] };
  },
  actions: {
    addSystemMessage(message: Message) {
      this.messages.push(message);
    },
    addUserMessage(message: Message) {
      this.messages.push(message);
    },
  },
});
