<script setup lang="ts">
import { computed } from 'vue'
import MarkdownIt from "markdown-it"
//import MarkdownItAbbr from "markdown-it-abbr"
import MarkdownItAnchor from "markdown-it-anchor"
//import MarkdownItFootnote from "markdown-it-footnote"
import MarkdownItHighlightjs from "markdown-it-highlightjs"
//import MarkdownItSub from "markdown-it-sub"
//import MarkdownItTasklists from "markdown-it-task-lists"
//import MarkdownItTOC from "markdown-it-toc-done-right"

const props = defineProps({
  source: {
    type: String,
    required: true
  }
})

const md = new MarkdownIt()
  .use(MarkdownItAnchor)
  .use(MarkdownItHighlightjs, {
    inline: true,
    auto: true,
    ignoreIllegals: true,
  })

const content = computed(() => md.render(props.source))
</script>

<template>
  <div v-html="content" />
</template>