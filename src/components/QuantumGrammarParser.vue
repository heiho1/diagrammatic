<template>
  <div class="quantum-grammar-parser">
    <!-- Input Section -->
    <q-card class="q-mb-md">
      <q-card-section>
        <h6 class="q-mt-none">Quantum Grammar Analysis</h6>
        <q-input
          v-model="sentence"
          filled
          label="Enter a sentence to analyze..."
          @keyup.enter="analyzeSentence"
          class="q-mb-md"
        />
        <div class="row q-gutter-md">
          <q-btn
            color="primary"
            label="Analyze with Quantum Grammar"
            @click="analyzeSentence"
            icon="analytics"
            :loading="loading"
            :disable="isAnalyzeDisabled"
          />
          <q-btn
            flat
            color="secondary"
            label="Clear"
            @click="clearAnalysis"
            icon="clear"
          />
        </div>
      </q-card-section>
    </q-card>

    <!-- Error Display -->
    <q-banner v-show="error" class="bg-red-2 q-mb-md">
      <template #avatar>
        <q-icon name="error" color="red" />
      </template>
      {{ error }}
      <template #action>
        <q-btn flat dense label="Dismiss" @click="error = null" />
      </template>
    </q-banner>

    <!-- Results Section -->
    <q-card v-show="parseResult" class="q-mb-md">
      <q-card-section>
        <h6 class="q-mt-none">Fact Establishment Analysis</h6>
        <div class="result-status">
          <div class="status-item">
            <span class="status-label">Communication Type:</span>
            <span
              :class="[
                'status-value',
                parseResult?.statistics?.communication_type === 'FACT-COMMUNICATION'
                  ? 'fact-communication'
                  : 'fictional-communication'
              ]"
            >
              {{ parseResult?.statistics?.communication_type || 'Unknown' }}
            </span>
          </div>
          <div class="status-item">
            <span class="status-label">Facts Established:</span>
            <span :class="['status-value', parseResult?.has_facts ? 'fact-yes' : 'fact-no']">
              {{ parseResult?.has_facts ? 'Yes (5,6,7 pattern found)' : 'No - Fictional language' }}
            </span>
          </div>
          <div class="status-item full-width">
            <span class="status-label">Analysis:</span>
            <span class="status-value">{{ parseResult?.fact_establishment }}</span>
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- Token Codes Display -->
    <q-card v-show="parseResult" class="q-mb-md">
      <q-card-section>
        <h6 class="q-mt-none">Token Analysis with Quantum Grammar Codes</h6>
        <div class="token-codes">
          <template v-for="token in parseResult?.tokens" :key="token.text">
            <div class="token-code-item">
              <span class="code-label">{{ token.text }}</span>
              <div class="code-info">
                <span :class="['code-value', `code-${token.code.split('.')[0]}`]">
                  {{ token.code }}
                </span>
                <span class="code-description">
                  {{ getCodeDescription(token.code) }}{{ getTenseInfo(token.code) }}
                </span>
              </div>
            </div>
          </template>
        </div>
      </q-card-section>
    </q-card>

    <!-- Code Legend -->
    <q-card v-show="parseResult" class="q-mb-md">
      <q-card-section>
        <h6 class="q-mt-none">Quantum Grammar Code Legend</h6>
        <div class="code-legend">
          <div class="legend-item">
            <span class="legend-code code-0">0</span>
            <span class="legend-text">CONJUNCTION (and, or)</span>
          </div>
          <div class="legend-item">
            <span class="legend-code code-1">1</span>
            <span class="legend-text">ADVERB</span>
          </div>
          <div class="legend-item">
            <span class="legend-code code-2">2</span>
            <span class="legend-text">VERB</span>
          </div>
          <div class="legend-item">
            <span class="legend-code code-3">3</span>
            <span class="legend-text">ADJECTIVE</span>
          </div>
          <div class="legend-item">
            <span class="legend-code code-4">4</span>
            <span class="legend-text">PRONOUN</span>
          </div>
          <div class="legend-item">
            <span class="legend-code code-5">5</span>
            <span class="legend-text">POSITION (prepositions)</span>
          </div>
          <div class="legend-item">
            <span class="legend-code code-6">6</span>
            <span class="legend-text">LODIAL (articles, determiners)</span>
          </div>
          <div class="legend-item">
            <span class="legend-code code-7">7</span>
            <span class="legend-text">FACT (noun)</span>
          </div>
          <div class="legend-item">
            <span class="legend-code code-8">8</span>
            <span class="legend-text">PAST-TIME-FICTION (add .8 suffix)</span>
          </div>
          <div class="legend-item">
            <span class="legend-code code-9">9</span>
            <span class="legend-text">FUTURE-TIME-FICTION (add .9 suffix)</span>
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- Modification Chain -->
    <q-card v-show="parseResult" class="q-mb-md">
      <q-card-section>
        <h6 class="q-mt-none">Modification Pattern</h6>
        <div class="modification-chain">
          <p class="chain-text">{{ parseResult?.modification_chain }}</p>
          <div class="chain-explanation">
            <p v-if="parseResult?.has_facts" class="explanation-item">
              <strong>5>6>7 Pattern:</strong> POSITION modifies LODIAL which modifies FACT - this
              establishes facts
            </p>
            <p class="explanation-item">
              <strong>Example:</strong> "For the healing" = POSITION(5) > LODIAL(6) > FACT(7)
            </p>
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- Statistics -->
    <q-card v-show="parseResult" class="q-mb-md">
      <q-card-section>
        <h6 class="q-mt-none">Statistics</h6>
        <div class="statistics-grid">
          <div class="stat-box">
            <div class="stat-label">Total Tokens</div>
            <div class="stat-value">{{ parseResult?.statistics?.token_count || 0 }}</div>
          </div>
          <div class="stat-box">
            <div class="stat-label">Code Distribution</div>
            <div class="stat-detail">
              <div v-for="(count, code) in parseResult?.statistics?.code_distribution" :key="code">
                Code {{ code }}: {{ count }} token(s)
              </div>
            </div>
          </div>
          <div class="stat-box">
            <div class="stat-label">Category Distribution</div>
            <div class="stat-detail">
              <div
                v-for="(count, category) in parseResult?.statistics?.category_distribution"
                :key="category"
              >
                {{ category }}: {{ count }}
              </div>
            </div>
          </div>
        </div>
      </q-card-section>
    </q-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const sentence = ref('')
const loading = ref(false)
const error = ref(null)
const parseResult = ref(null)

const API_BASE_URL = 'http://localhost:5000/api'

const codeDescriptions = {
  '0': 'Conjunction (and, or)',
  '1': 'Adverb (modifier)',
  '2': 'Verb (action/being)',
  '3': 'Adjective (descriptor)',
  '4': 'Pronoun (indefinite)',
  '5': 'Position (spatial/relational)',
  '6': 'Lodial (ownership/article)',
  '7': 'Fact (noun/established)',
  '8': 'Past-time (historical)',
  '9': 'Future-time (projected)'
}

const getCodeDescription = (code) => {
  const baseCode = code.split('.')[0]
  return codeDescriptions[baseCode] || 'Unknown'
}

const getTenseInfo = (code) => {
  if (code.includes('.8')) {
    return ' (Past-tense)'
  }
  if (code.includes('.9')) {
    return ' (Future-tense)'
  }
  return ''
}

const isAnalyzeDisabled = computed(() => {
  return !sentence.value.trim() || loading.value
})

const analyzeSentence = async () => {
  if (!sentence.value.trim()) {
    return
  }

  error.value = null
  loading.value = true
  parseResult.value = null

  try {
    const response = await fetch(`${API_BASE_URL}/parse-quantum-grammar`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        text: sentence.value.trim()
      })
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.error || 'Failed to analyze sentence')
    }

    const data = await response.json()

    if (!data.success) {
      throw new Error(data.error || 'Analysis failed')
    }

    parseResult.value = data
  } catch (err) {
    error.value = `Error: ${err.message}`
    console.error('Analysis error:', err)
  } finally {
    loading.value = false
  }
}

const clearAnalysis = () => {
  sentence.value = ''
  parseResult.value = null
  error.value = null
}
</script>

<style scoped>
.quantum-grammar-parser {
  max-width: 1200px;
  margin: 0 auto;
}

.result-status {
  display: flex;
  flex-direction: column;
  gap: 15px;
  background-color: #f5f5f5;
  padding: 15px;
  border-radius: 4px;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.status-item.full-width {
  flex-direction: column;
  align-items: flex-start;
}

.status-label {
  font-weight: bold;
  min-width: 180px;
}

.status-value {
  padding: 6px 12px;
  border-radius: 3px;
  font-weight: 500;
}

.fact-communication {
  background-color: #c8e6c9;
  color: #2e7d32;
}

.fictional-communication {
  background-color: #ffccbc;
  color: #d84315;
}

.fact-yes {
  background-color: #a5d6a7;
  color: #1b5e20;
}

.fact-no {
  background-color: #ef9a9a;
  color: #c62828;
}

.token-codes {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  background-color: #fafafa;
  padding: 15px;
  border-radius: 4px;
}

.token-code-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 140px;
  text-align: center;
}

.code-label {
  font-weight: bold;
  font-size: 15px;
  color: #333;
  padding-bottom: 4px;
  border-bottom: 2px solid #f0f0f0;
  width: 100%;
}

.code-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  width: 100%;
}

.code-value {
  font-size: 20px;
  font-weight: bold;
  padding: 6px 10px;
  border-radius: 3px;
  color: white;
  min-width: 45px;
}

.code-description {
  font-size: 12px;
  color: #666;
  font-weight: 500;
  line-height: 1.3;
  word-break: break-word;
}

.code-0 {
  background-color: #9c27b0;
}
.code-1 {
  background-color: #e91e63;
}
.code-2 {
  background-color: #f44336;
}
.code-3 {
  background-color: #ff9800;
}
.code-4 {
  background-color: #ffc107;
}
.code-5 {
  background-color: #2196f3;
}
.code-6 {
  background-color: #009688;
}
.code-7 {
  background-color: #4caf50;
}

.code-category {
  font-size: 11px;
  color: #666;
  font-weight: 500;
}

.code-legend {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
  background-color: #fafafa;
  padding: 15px;
  border-radius: 4px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.legend-code {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 4px;
  color: white;
  font-weight: bold;
  font-size: 14px;
}

.legend-text {
  flex: 1;
  font-size: 14px;
}

.modification-chain {
  background-color: #f5f5f5;
  padding: 15px;
  border-radius: 4px;
}

.chain-text {
  font-family: monospace;
  background-color: white;
  padding: 10px;
  border-left: 3px solid #2196f3;
  margin: 0 0 15px 0;
  word-break: break-word;
}

.chain-explanation {
  margin-top: 10px;
}

.explanation-item {
  margin: 8px 0;
  font-size: 14px;
  line-height: 1.5;
}

.statistics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
}

.stat-box {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
  border-radius: 4px;
  text-align: center;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
}

.stat-detail {
  font-size: 12px;
  text-align: left;
  line-height: 1.6;
}
</style>
