<template>
  <q-layout view="lHh LpR lFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-toolbar-title>
          🎓 Diagrammatic - Sentence Diagramming Tool
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <q-page class="q-pa-lg">
        <q-tabs
          v-model="activeTab"
          dense
          class="text-primary q-mb-lg"
          active-color="primary"
          indicator-color="primary"
          align="left"
        >
          <q-tab name="stanza" label="Stanza Parser (Standard)" />
          <q-tab name="quantum-grammar" label="Quantum Grammar Parser" />
        </q-tabs>

        <!-- Stanza Parser Tab -->
        <q-tab-panels v-model="activeTab" animated>
          <q-tab-panel name="stanza">
            <SentenceDiagrammer />
          </q-tab-panel>

          <!-- Quantum Grammar Parser Tab -->
          <q-tab-panel name="quantum-grammar">
            <QuantumGrammarParser />
          </q-tab-panel>
        </q-tab-panels>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import SentenceDiagrammer from '@/components/SentenceDiagrammer.vue'
import QuantumGrammarParser from '@/components/QuantumGrammarParser.vue'

const activeTab = ref('stanza')
</script>

<style scoped>
</style>
