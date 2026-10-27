import { ref, watch, type Ref } from 'vue'
import { type Search, type Ticket } from './api'
export function useTicketSearch(query: Ref<string>, search: Search) {
  const rows=ref<Ticket[]>([]), loading=ref(false), error=ref('')
  watch(query, async (value,_old,onCleanup) => {
    const controller=new AbortController()
    let active=true
    onCleanup(()=>{active=false;controller.abort()})
    loading.value=true;error.value=''
    try {
      const result=await search(value,controller.signal)
      if(active) rows.value=result
    } catch(e) {
      if(active) error.value=e instanceof Error?e.message:'Search failed'
    } finally { if(active) loading.value=false }
  },{immediate:true})
  return {rows,loading,error}
}
