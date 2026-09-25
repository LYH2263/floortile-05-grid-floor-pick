<script setup>
import { computed } from 'vue'

const props = defineProps({
  cols: { type: Number, default: 0 },
  rows: { type: Number, default: 0 },
  gridCount: { type: Number, default: 0 },
  rawCount: { type: Number, default: null },
  wastePct: { type: Number, default: 0 },
  maxMode: { type: Boolean, default: false },
})

const withWaste = (base) => Math.ceil(base * (1 + props.wastePct / 100) - 1e-9)

const compare = computed(() => {
  if (props.rawCount == null) return null
  const picked = props.maxMode ? Math.max(props.rawCount, props.gridCount) : props.rawCount
  return {
    areaOrder: withWaste(props.rawCount),
    gridOrder: withWaste(props.gridCount),
    picked,
  }
})
</script>
<template>
  <div class="grid-preview">
    <p>铺砖网格预览：{{ cols }} 列 × {{ rows }} 行，共 {{ gridCount }} 块（含裁切格）</p>
    <div class="mini-grid" :style="{ gridTemplateColumns: `repeat(${Math.min(cols, 12)}, 1fr)` }">
      <span v-for="n in Math.min(cols * rows, 48)" :key="n" class="cell"></span>
    </div>
    <ul v-if="compare" class="max-mode-compare">
      <li :class="{ picked: maxMode && compare.picked === gridCount }">
        网格块数 {{ gridCount }} 块 → 含损耗 {{ compare.gridOrder }} 片
      </li>
      <li :class="{ picked: !maxMode || compare.picked === rawCount }">
        面积法 {{ rawCount }} 片 → 含损耗 {{ compare.areaOrder }} 片
      </li>
      <li>当前模式：{{ maxMode ? '择大（选用基数 ' + compare.picked + '）' : '面积法（选用基数 ' + compare.picked + '）' }}</li>
    </ul>
  </div>
</template>
