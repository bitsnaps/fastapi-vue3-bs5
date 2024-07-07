// vite.config.js/ts
import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import Components from 'unplugin-vue-components/vite'
import AutoImport from 'unplugin-auto-import/vite'
import { BootstrapVueNextResolver } from 'bootstrap-vue-next'
// import VueMacros from 'unplugin-vue-macros/vite'

export default defineConfig({
  plugins: [
    vue(),
    Components({
      resolvers: [BootstrapVueNextResolver()],      
        // allow auto load markdown components under `./src/components/`
        extensions: ['vue', 'md'],
        // allow auto import and register components used in markdown
        include: [/\.vue$/, /\.vue\?vue/, /\.md$/]
      }),
    AutoImport({ imports: ['vue','vue-router'] }),
    // Not stable yet enough
    // VueMacros({
    //   plugins: {
    //     vue: Vue(),
    //     // vueJsx: VueJsx(), // if needed
    //   },
    // }),
  ],
})