<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, putJSON } from '../api'

const settings = ref({})
const defaultMaxMode = ref(false)
const saved = ref('')
const err = ref('')

onMounted(async () => {
  settings.value = await getJSON('/api/settings')
  defaultMaxMode.value = settings.value.max_mode === '1' || settings.value.max_mode === 'true'
})

async function saveDefault() {
  saved.value = ''
  err.value = ''
  try {
    settings.value = await putJSON('/api/settings', { max_mode: defaultMaxMode.value })
    saved.value = '已保存默认择大设置（仅影响新测算，不影响历史记录）'
  } catch (e) {
    err.value = e.message
  }
}
</script>
<template>
  <div class="page">
    <h1>损耗规则</h1>
    <p>默认损耗率按面积法向上取整后再乘 (1+损耗%)。</p>
    <p>当前默认损耗：<strong>{{ settings.waste_pct }}%</strong></p>
    <p>网格预览块数可能大于面积法片数；开启择大后，订货基数取面积法与网格块数较大者，下单以 order_count 为准。</p>
    <label class="inline">
      <input type="checkbox" v-model="defaultMaxMode" /> 默认开启择大订货
    </label>
    <button @click="saveDefault">保存默认</button>
    <p v-if="saved" class="ok">{{ saved }}</p>
    <p v-if="err" class="alert">{{ err }}</p>
  </div>
</template>
