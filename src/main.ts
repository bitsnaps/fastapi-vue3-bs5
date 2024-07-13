// main.js/ts
import { createApp } from "vue";
import { createBootstrap } from "bootstrap-vue-next";
import App from "./App.vue";
import { createPinia } from "pinia";
import { createI18n } from "vue-i18n";
import router from "./router";

// Add the necessary CSS
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue-next/dist/bootstrap-vue-next.css";

const pinia = createPinia();
const i18n = createI18n({
  locale: "en",
  fallbackLocale: "en",
  messages: {
    en: {
      message: {
        hello: "Hello",
      },
    },
    fr: {
      message: {
        hello: "Bonjour",
      },
    },
  },
});
const app = createApp(App);
app.use(pinia);
app.use(router);
app.use(i18n);
app.use(createBootstrap());
app.mount("#app");
