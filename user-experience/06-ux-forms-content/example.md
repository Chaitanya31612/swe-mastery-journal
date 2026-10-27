## Follow a concrete example

```html
<label for="followup">Follow-up date</label>
<input id="followup" type="date" aria-describedby="followup-help followup-error">
<p id="followup-help">Use the team’s working time zone: Asia/Kolkata.</p>
<p id="followup-error">Choose today or a later date.</p>
```
Render the error only when relevant and keep it associated with the field. For a rejected form, preserve values and provide a useful error summary when several fields need attention.