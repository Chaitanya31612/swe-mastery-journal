import { describe,it,expect } from 'vitest'
import { mount,flushPromises } from '@vue/test-utils'
import TicketWorkspace from './TicketWorkspace.vue'
import type { Ticket } from './api'
function deferred() { let resolve!:(rows:Ticket[])=>void, reject!:(e:Error)=>void;const promise=new Promise<Ticket[]>((yes,no)=>{resolve=yes;reject=no});return {promise,resolve,reject} }
const row=(title:string):Ticket=>({id:'1',title,tags:['support']})
describe('ticket workspace boundaries',()=>{
  it('does not accept a stale success or clear the current loading state',async()=>{
    const a=deferred(),b=deferred();let count=0
    const wrapper=mount(TicketWorkspace,{props:{search:()=>count++===0?a.promise:b.promise}})
    await wrapper.get('#query').setValue('new')
    a.resolve([row('Old')]);await flushPromises()
    expect(wrapper.text()).toContain('Searching…');expect(wrapper.text()).not.toContain('Old')
    b.resolve([row('New')]);await flushPromises()
    expect(wrapper.text()).toContain('New');expect(wrapper.text()).not.toContain('Searching…');wrapper.unmount()
  })
  it('does not replace a newer result with an obsolete error',async()=>{
    const a=deferred(),b=deferred();let count=0
    const wrapper=mount(TicketWorkspace,{props:{search:()=>count++===0?a.promise:b.promise}})
    await wrapper.get('#query').setValue('new');b.resolve([row('New')]);await flushPromises()
    a.reject(new Error('Old error'));await flushPromises()
    expect(wrapper.text()).toContain('New');expect(wrapper.find('[role=alert]').exists()).toBe(false);wrapper.unmount()
  })
  it('cancel preserves saved data and save deliberately accepts a trimmed edit',async()=>{
    const wrapper=mount(TicketWorkspace,{props:{search:async()=>[row('Original')]}});await flushPromises()
    await wrapper.get('li button').trigger('click');await wrapper.get('#title').setValue('Unsaved')
    await wrapper.get('button[type=button]').trigger('click');expect(wrapper.get('li').text()).toContain('Original')
    await wrapper.get('li button').trigger('click');await wrapper.get('#title').setValue('  Saved title  ');await wrapper.get('form').trigger('submit')
    expect(wrapper.get('li').text()).toContain('Saved title');expect(wrapper.find('form').exists()).toBe(false);wrapper.unmount()
  })
})
