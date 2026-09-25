<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
const openId = ref(null)
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
function toggle(id) { openId.value = openId.value === id ? null : id }
// 还原 run 保存时的口径：旧记录没有 take_max/base_count 字段时按面积法展示
function modeOf(r) { return r.result?.take_max ? '择大' : '面积法' }
function baseOf(r) { return r.result?.base_count ?? r.result?.raw_count }
</script>
<template>
  <div class="page">
    <h1>测算记录</h1>
    <table class="tbl">
      <thead><tr><th>时间</th><th>房间</th><th>砖型</th><th>模式</th><th>片数</th></tr></thead>
      <tbody>
        <template v-for="r in items" :key="r.id">
          <tr class="run-row" @click="toggle(r.id)">
            <td>{{ r.created_at?.slice(0, 19) }}</td>
            <td>{{ r.room_name }}</td>
            <td>{{ r.tile_name }}</td>
            <td>{{ modeOf(r) }}</td>
            <td>{{ r.result?.order_count }}</td>
          </tr>
          <tr v-if="openId === r.id" class="run-detail">
            <td colspan="5">
              订货基数 {{ baseOf(r) }} 片（{{ modeOf(r) }}），
              面积法净用量 {{ r.result?.raw_count }} 片，
              网格块数 {{ r.result?.layout?.grid_count ?? '—' }} 块，
              损耗 {{ r.result?.waste_pct }}%，
              订货 {{ r.result?.order_count }} 片
              <span v-if="r.note">；备注：{{ r.note }}</span>
            </td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
</template>
