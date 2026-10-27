## Understand the idea

A browser receives values, not intentions. A missing field can mean “leave unchanged.” null can mean “clear it.” false and zero can be valid choices. Decide those meanings in the API contract before choosing a default operator.

Use ?? when the fallback should apply to null or undefined. Use || only when all falsey values should trigger the fallback. Destructuring and spread copy one level. A new outer object may still share nested objects with the original. That can make Cancel accidentally change the saved record.

Treat JSON as outside input. JSON.parse proves that text is valid JSON; it does not prove that the result has a ticket ID, an allowed status, or a sensible array shape. Validate at the boundary, then pass a stable internal shape to components.
