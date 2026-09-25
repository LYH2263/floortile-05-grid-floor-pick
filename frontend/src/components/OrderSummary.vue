<script setup>
defineProps({
  result: { type: Object, default: null },
})
</script>
<template>
  <div v-if="result" class="order-summary">
    <div class="hero">{{ result.order_count }} 片</div>
    <ul>
      <li>面积法净用量 {{ result.raw_count }} 片，网格块数 {{ result.grid_count }} 块</li>
      <li>
        订货基数 {{ result.order_base }} 片
        <span v-if="result.max_mode" class="mode-badge">择大：取面积法与网格较大者</span>
        <span v-else class="mode-badge off">面积法</span>
        ，损耗 {{ result.waste_pct }}%
      </li>
      <li>地面 {{ result.area_m2 }} m²，单砖 {{ result.piece_m2 }} m²</li>
    </ul>
  </div>
</template>
