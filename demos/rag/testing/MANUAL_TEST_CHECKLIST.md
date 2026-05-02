# Manual Test Checklist

## Website

- [ ] Homepage loads
- [ ] Services section visible
- [ ] Chat widget visible
- [ ] Chat opens
- [ ] Chat closes
- [ ] Message sends
- [ ] Loading state appears
- [ ] Response appears
- [ ] Citations appear
- [ ] Escalation message appears when expected
- [ ] Mobile width is usable

## Backend

- [ ] GET /health works
- [ ] POST /chat works
- [ ] Empty input handled cleanly
- [ ] Unsupported question handled cleanly
- [ ] Outcome log created
- [ ] Escalation log created when expected
