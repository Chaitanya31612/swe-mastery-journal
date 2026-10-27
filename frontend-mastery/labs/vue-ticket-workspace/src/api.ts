export type Ticket = { id: string; title: string; tags: string[] }
export type Search = (query: string, signal: AbortSignal) => Promise<Ticket[]>
const source: Ticket[] = [
  {id:'1',title:'Export is slow',tags:['reporting']},
  {id:'2',title:'Cannot upload a file',tags:['files']},
]
// Synthetic API. The timer only makes waiting visible; tests control promises.
export const searchTickets: Search = (query, signal) => new Promise((resolve,reject) => {
  const timer=setTimeout(()=>resolve(source.filter(t=>t.title.toLowerCase().includes(query.toLowerCase()))),350)
  signal.addEventListener('abort',()=>{clearTimeout(timer);reject(new DOMException('Aborted','AbortError'))},{once:true})
})
