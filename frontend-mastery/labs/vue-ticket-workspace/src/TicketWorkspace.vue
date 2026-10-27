<script setup lang="ts">
import { ref } from 'vue'
import { searchTickets, type Search, type Ticket } from './api'
import { useTicketSearch } from './useTicketSearch'
const props=defineProps<{search?:Search}>()
const query=ref(''), draft=ref<Ticket|null>(null), saved=ref<Ticket|null>(null)
const {rows,loading,error}=useTicketSearch(query,props.search??searchTickets)
function edit(ticket:Ticket) { saved.value=ticket;draft.value={...ticket,tags:[...ticket.tags]} }
function save() {
  if(!draft.value?.title.trim()) return
  if(saved.value) { saved.value.title=draft.value.title.trim();saved.value.tags=[...draft.value.tags] }
  draft.value=null
}
</script>
<template>
  <main>
    <h1>Support tickets</h1><p>Search, edit a title, or cancel. All data is synthetic and stays in memory.</p>
    <label for="query">Search tickets</label><input id="query" v-model="query" type="search"/>
    <p role="status">{{ loading?'Searching…':`${rows.length} matching tickets` }}</p>
    <p v-if="error" role="alert">{{ error }}. Change the search to try again.</p>
    <ul><li v-for="ticket in rows" :key="ticket.id"><span>{{ ticket.title }}</span> <button @click="edit(ticket)">Edit {{ ticket.id }}</button></li></ul>
    <form v-if="draft" @submit.prevent="save">
      <h2>Edit ticket {{ draft.id }}</h2><label for="title">Ticket title</label><input id="title" v-model="draft.title" required aria-describedby="title-help"/>
      <p id="title-help">Use a short title that explains the problem.</p><button type="submit">Save title</button><button type="button" @click="draft=null">Cancel</button>
    </form>
    <p>This lab focuses on request ownership and independent drafts. A production editor also needs authorization, optimistic-concurrency handling, focus restoration, and persistence.</p>
  </main>
</template>
<style>
body{font:18px/1.6 system-ui;color:#153047;background:#f1f5f9;margin:0}main{max-width:760px;margin:40px auto;padding:24px}input,button{font:inherit;padding:10px;margin:6px;border:1px solid #64748b;border-radius:6px}input{display:block;max-width:90%}button{cursor:pointer;background:white}button:focus-visible,input:focus-visible{outline:3px solid #007d96;outline-offset:3px}form{border:1px solid #64748b;padding:20px}li{margin:14px 0}
</style>
