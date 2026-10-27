# A small example

```html
<label for="task-title">Task title</label>
<input id="task-title" aria-describedby="title-help title-error">
<p id="title-help">Use a short action, such as “Review the report”.</p>
<p id="title-error" role="alert">Enter a title before saving.</p>
<button type="button">Save task</button>
<p role="status" aria-live="polite">Saving…</p>
```
Show the error/status only when relevant. Do not announce every keystroke.

In the capstone, test keyboard use, small screens, slow responses, and failed saves.