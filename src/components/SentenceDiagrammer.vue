<template>
  <div class="sentence-diagrammer">
    <!-- Input Section -->
    <q-card class="q-mb-md">
      <q-card-section>
        <h6 class="q-mt-none">Enter a Sentence to Diagram</h6>
        <q-input
          v-model="sentence"
          filled
          label="Type your sentence here..."
          @keyup.enter="diagramSentence"
          class="q-mb-md"
        />
        <div class="row q-gutter-md">
          <q-btn
            color="primary"
            label="Analyze & Diagram"
            @click="diagramSentence"
            icon="analytics"
            :loading="loading"
            :disable="isAnalyzeDisabled"
          />
          <q-select
            v-model="selectedLanguage"
            :options="languageOptions"
            label="Language (auto-detect if not set)"
            class="col-auto"
            outlined
            dense
            clearable
            emit-value
            map-options
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

    <!-- Dependency Tree Diagram -->
    <q-card v-show="parseResult" class="q-mb-md">
      <q-card-section>
        <h6 class="q-mt-none">Dependency Tree</h6>
        <div class="diagram-container">
          <canvas ref="diagramCanvas" class="diagram-canvas"></canvas>
        </div>
      </q-card-section>
    </q-card>

    <!-- Token Details Table -->
    <q-card v-show="parseResult" class="q-mb-md">
      <q-card-section>
        <h6 class="q-mt-none">Token Analysis</h6>
        <q-table
          :rows="tableRows"
          :columns="tokenColumns"
          row-key="id"
          flat
          bordered
          dense
        >
          <template #body-cell-text="props">
            <q-td :props="props">
              <strong>{{ props.row.text }}</strong>
            </q-td>
          </template>
          <template #body-cell-upos="props">
            <q-td :props="props">
              <div class="tag-cell">
                <span class="tag-code">{{ props.row.upos }}</span>
                <span class="tag-description">{{ getPosDescription(props.row.upos) }}</span>
              </div>
            </q-td>
          </template>
          <template #body-cell-deprel="props">
            <q-td :props="props">
              <div class="tag-cell">
                <span class="tag-code">{{ props.row.deprel }}</span>
                <span class="tag-description">{{ getDeprelDescription(props.row.deprel) }}</span>
              </div>
            </q-td>
          </template>
        </q-table>
      </q-card-section>
    </q-card>

    <!-- Statistics -->
    <q-card v-show="statistics" class="q-mb-md">
      <q-card-section>
        <h6 class="q-mt-none">Statistics</h6>
        <div class="row q-col-gutter-md">
          <div class="col-12 col-sm-6">
            <div class="stat-box">
              <div class="stat-label">Tokens</div>
              <div class="stat-value">{{ tokenCount }}</div>
            </div>
          </div>
          <div class="col-12 col-sm-6">
            <div class="stat-box">
              <div class="stat-label">Sentences</div>
              <div class="stat-value">{{ sentenceCount }}</div>
            </div>
          </div>
        </div>
        <div v-if="statistics" class="q-mt-md">
          <h6>POS Distribution</h6>
          <div v-for="(count, pos) in posDistribution" :key="pos" class="q-mb-md">
            <div class="text-caption q-mb-xs">{{ pos }}: {{ count }}</div>
            <q-linear-progress
              :value="getProgressValue(count)"
              color="primary"
            />
          </div>
        </div>
      </q-card-section>
    </q-card>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

const sentence = ref('')
const selectedLanguage = ref(null)
const loading = ref(false)
const error = ref(null)
const parseResult = ref(null)
const statistics = ref(null)
const diagramCanvas = ref(null)

const API_BASE_URL = 'http://localhost:5000/api'

const languageOptions = [
  { label: 'English', value: 'en' },
  { label: 'Spanish', value: 'es' },
  { label: 'French', value: 'fr' },
  { label: 'German', value: 'de' },
  { label: 'Italian', value: 'it' },
  { label: 'Portuguese', value: 'pt' },
  { label: 'Russian', value: 'ru' },
  { label: 'Chinese', value: 'zh' },
  { label: 'Japanese', value: 'ja' },
  { label: 'Arabic', value: 'ar' },
  { label: 'Turkish', value: 'tr' },
  { label: 'Ukrainian', value: 'uk' },
  { label: 'Polish', value: 'pl' },
  { label: 'Dutch', value: 'nl' },
  { label: 'Swedish', value: 'sv' },
  { label: 'Vietnamese', value: 'vi' },
  { label: 'Thai', value: 'th' },
  { label: 'Hindi', value: 'hi' }
]

const tokenColumns = [
  { name: 'text', label: 'Word', field: 'text', align: 'left' },
  { name: 'lemma', label: 'Lemma', field: 'lemma', align: 'left' },
  { name: 'upos', label: 'POS', field: 'upos', align: 'left' },
  { name: 'deprel', label: 'Dependency', field: 'deprel', align: 'left' },
  { name: 'head', label: 'Head Index', field: 'head', align: 'center' }
]

// POS tag descriptions (Universal POS tags)
const posDescriptions = {
  'ADJ': 'Adjective - describes nouns',
  'ADP': 'Adposition - prepositions/postpositions',
  'ADV': 'Adverb - modifies verbs/adjectives',
  'AUX': 'Auxiliary - helping verbs',
  'CCONJ': 'Coordinating conjunction - connects equals',
  'DET': 'Determiner - articles/demonstratives',
  'INTJ': 'Interjection - exclamations',
  'NOUN': 'Noun - person/place/thing',
  'NUM': 'Numeral - numbers/quantities',
  'PART': 'Particle - function words',
  'PRON': 'Pronoun - replaces noun',
  'PROPN': 'Proper noun - specific names',
  'PUNCT': 'Punctuation - marks',
  'SCONJ': 'Subordinating conjunction - connects clauses',
  'SYM': 'Symbol - non-word symbols',
  'VERB': 'Verb - action/state',
  'X': 'Other - unclassified'
}

// Dependency relation descriptions
const deprelDescriptions = {
  'nsubj': 'Nominal subject',
  'nsubj:pass': 'Nominal subject (passive)',
  'csubj': 'Clausal subject',
  'csubj:pass': 'Clausal subject (passive)',
  'obj': 'Direct object',
  'iobj': 'Indirect object',
  'ccomp': 'Clausal complement',
  'xcomp': 'Open clausal complement',
  'obl': 'Oblique nominal',
  'vocative': 'Vocative',
  'expl': 'Expletive',
  'dislocated': 'Dislocated',
  'advcl': 'Adverbial clause',
  'advmod': 'Adverbial modifier',
  'discourse': 'Discourse element',
  'aux': 'Auxiliary',
  'cop': 'Copula',
  'mark': 'Marker',
  'nmod': 'Nominal modifier',
  'nmod:poss': 'Possessive nominal modifier',
  'nmod:tmod': 'Temporal nominal modifier',
  'appos': 'Appositional modifier',
  'acl': 'Adjectival clause',
  'acl:relcl': 'Relative clause',
  'amod': 'Adjectival modifier',
  'det': 'Determiner',
  'det:poss': 'Possessive determiner',
  'case': 'Case marker',
  'clf': 'Classifier',
  'compound': 'Compound',
  'compound:prt': 'Particle for phrasal verb',
  'mwe': 'Multi-word expression',
  'flat': 'Flat multi-word name',
  'flat:name': 'Flat name',
  'conj': 'Conjunct',
  'list': 'List',
  'parataxis': 'Parataxis',
  'orphan': 'Orphan',
  'goeswith': 'Goes with',
  'root': 'Root of tree',
  'dep': 'Unspecified dependency',
  'cc': 'Coordinating conjunction'
}

const getPosDescription = (pos) => {
  return posDescriptions[pos] || pos
}

const getDeprelDescription = (deprel) => {
  return deprelDescriptions[deprel] || deprel
}

const isAnalyzeDisabled = computed(() => {
  return !sentence.value.trim() || loading.value
})

const tableRows = computed(() => {
  return parseResult.value?.tokens || []
})

const tokenCount = computed(() => {
  return statistics.value?.token_count || 0
})

const sentenceCount = computed(() => {
  return statistics.value?.sentence_count || 0
})

const posDistribution = computed(() => {
  return statistics.value?.pos_distribution || {}
})

const getProgressValue = (count) => {
  const total = statistics.value?.token_count || 1
  return count / total
}

const diagramSentence = async () => {
  if (!sentence.value.trim()) {
    return
  }

  error.value = null
  loading.value = true
  parseResult.value = null
  statistics.value = null

  try {
    const payload = {
      text: sentence.value.trim()
    }

    if (selectedLanguage.value) {
      payload.language = selectedLanguage.value
    }

    const response = await fetch(`${API_BASE_URL}/parse-detailed`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.error || 'Failed to parse sentence')
    }

    const data = await response.json()

    if (!data.result.success) {
      throw new Error(data.result.error || 'NLP parsing failed')
    }

    parseResult.value = data.result
    statistics.value = data.statistics

    // Draw the dependency tree diagram
    await drawDependencyTree()
  } catch (err) {
    error.value = `Error: ${err.message}`
    console.error('Parse error:', err)
  } finally {
    loading.value = false
  }
}

const drawDependencyTree = () => {
  return new Promise((resolve) => {
    if (!diagramCanvas.value || !parseResult.value || !parseResult.value.tokens) {
      resolve()
      return
    }

    const canvas = diagramCanvas.value
    const ctx = canvas.getContext('2d')
    const tokens = parseResult.value.tokens

    // Set canvas size
    const padding = 60
    const canvasWidth = Math.max(1000, tokens.length * 80)
    const canvasHeight = 400

    canvas.width = canvasWidth
    canvas.height = canvasHeight

    // Clear canvas
    ctx.fillStyle = '#ffffff'
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    // Position tokens horizontally
    const spacing = (canvasWidth - 2 * padding) / Math.max(1, tokens.length - 1)
    const baselineY = 300
    const tokenHeight = 80

    // Draw dependencies first (so they appear behind tokens)
    ctx.strokeStyle = '#999999'
    ctx.fillStyle = '#666666'
    ctx.font = 'italic 12px Arial'

    tokens.forEach((token, index) => {
      if (token.deprel === 'root') return

      const fromX = padding + index * spacing
      const fromY = baselineY

      const headIndex = token.head - 1
      if (headIndex >= 0 && headIndex < tokens.length) {
        const toX = padding + headIndex * spacing
        const toY = baselineY

        // Draw arc
        const arcHeight = Math.abs(toX - fromX) / 2.5
        ctx.beginPath()
        ctx.moveTo(fromX, fromY)

        // Create quadratic curve
        const controlX = (fromX + toX) / 2
        const controlY = Math.min(baselineY - arcHeight, baselineY - 60)
        ctx.quadraticCurveTo(controlX, controlY, toX, toY)
        ctx.stroke()

        // Draw arrow head
        const angle = Math.atan2(toY - controlY, toX - controlX)
        const arrowSize = 10
        ctx.fillStyle = '#666666'
        ctx.beginPath()
        ctx.moveTo(toX, toY)
        ctx.lineTo(toX - arrowSize * Math.cos(angle - Math.PI / 6), toY - arrowSize * Math.sin(angle - Math.PI / 6))
        ctx.lineTo(toX - arrowSize * Math.cos(angle + Math.PI / 6), toY - arrowSize * Math.sin(angle + Math.PI / 6))
        ctx.fill()

        // Draw dependency label
        const labelX = (fromX + toX) / 2
        const labelY = controlY - 10
        ctx.fillStyle = '#666666'
        ctx.textAlign = 'center'
        ctx.fillText(token.deprel, labelX, labelY)
      }
    })

    // Draw tokens
    ctx.fillStyle = '#1976d2'
    ctx.strokeStyle = '#0d47a1'
    ctx.lineWidth = 2

    tokens.forEach((token, index) => {
      const x = padding + index * spacing
      const y = baselineY + tokenHeight / 2

      // Draw token box
      const boxWidth = 70
      const boxHeight = 35
      ctx.fillRect(x - boxWidth / 2, y - boxHeight / 2, boxWidth, boxHeight)
      ctx.strokeRect(x - boxWidth / 2, y - boxHeight / 2, boxWidth, boxHeight)

      // Draw text
      ctx.fillStyle = '#ffffff'
      ctx.font = 'bold 13px Arial'
      ctx.textAlign = 'center'
      ctx.textBaseline = 'middle'
      ctx.fillText(token.text, x, y - 8)

      ctx.fillStyle = '#0d47a1'
      ctx.font = '10px Arial'
      ctx.fillText(token.upos, x, y + 8)
    })

    // Draw root indicator
    const rootToken = tokens.find(t => t.deprel === 'root')
    if (rootToken) {
      const rootIndex = tokens.indexOf(rootToken)
      const x = padding + rootIndex * spacing
      const y = baselineY + tokenHeight / 2

      ctx.strokeStyle = '#ff6f00'
      ctx.lineWidth = 3
      ctx.strokeRect(x - 40, y - 20, 80, 40)
    }

    resolve()
  })
}

watch(sentence, () => {
  parseResult.value = null
  statistics.value = null
})
</script>

<style scoped>
.sentence-diagrammer {
  max-width: 1200px;
  margin: 0 auto;
}

.diagram-container {
  overflow-x: auto;
  background-color: #fafafa;
  border: 1px solid #cccccc;
  border-radius: 4px;
  padding: 10px;
}

.diagram-canvas {
  display: block;
  margin: 0 auto;
}

.tag-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.tag-code {
  font-weight: bold;
  font-size: 13px;
  color: #1976d2;
  font-family: monospace;
}

.tag-description {
  font-size: 12px;
  color: #666;
  font-style: italic;
  line-height: 1.3;
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
</style>
