## Follow a concrete example

```ts
// Vue Test Utils / Vitest sketch; imports and the component are project setup.
const wrapper = mount(TicketForm, { props: { initialTitle: 'Old' } })
await wrapper.get('input').setValue('New')
await wrapper.get('form').trigger('submit')
await flushPromises()
expect(wrapper.get('input').element.value).toBe('New')
expect(wrapper.text()).toContain('Your edits are kept')
```
Configure the fake request to reject before asserting this case. Assert the contract and user-visible result rather than every internal ref name.