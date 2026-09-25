<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'

const items = ref([])
const detail = ref(null)

onMounted(async () => { items.value = (await getJSON('/api/runs')).items })

function modeOf(result) {
  // legacy runs saved before the max-mode change have no flag -> area method
  return result?.max_mode ? '择大' : '面积法'
}

async function open(run) {
  const row = await getJSON(`/api/runs/${run.id}`)
  const r = row.result || {}
  detail.value = {
    ...row,
    maxMode: !!r.max_mode,
    rawCount: r.raw_count,
    gridCount: r.grid_count ?? r.layout?.grid_count,
    orderBase: r.order_base ?? r.raw_count,
    orderCount: r.order_count,
    wastePct: r.waste_pct ?? row.waste_pct,
  }
}

function close() {
  detail.value = null
}
</script>
<template>
  <div class="page">
    <h1>测算记录</h1>
    <table class="tbl">
      <thead><tr><th>时间</th><th>房间</th><th>砖型</th><th>模式</th><th>片数</th><th></th></tr></thead>
      <tbody>
        <tr v-for="r in items" :key="r.id">
          <td>{{ r.created_at?.slice(0, 19) }}</td>
          <td>{{ r.room_name }}</td>
          <td>{{ r.tile_name }}</td>
          <td>{{ modeOf(r.result) }}</td>
          <td>{{ r.result?.order_count }}</td>
          <td><button @click="open(r)">详情</button></td>
        </tr>
      </tbody>
    </table>

    <div v-if="detail" class="run-detail">
      <h2>记录 #{{ detail.id }}</h2>
      <p>
        {{ detail.room_name }} / {{ detail.tile_name }}，
        订货模式：<strong>{{ detail.maxMode ? '择大（取面积法与网格较大者）' : '面积法' }}</strong>
      </p>
      <ul>
        <li>面积法净用量：{{ detail.rawCount }} 片</li>
        <li>网格块数：{{ detail.gridCount }} 块</li>
        <li>选用基数：{{ detail.orderBase }} 片</li>
        <li>损耗 {{ detail.wastePct }}% 后订货片数：<strong>{{ detail.orderCount }} 片</strong></li>
      </ul>
      <button @click="close">关闭</button>
    </div>
  </div>
</template>
