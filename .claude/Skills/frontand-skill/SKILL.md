---
name: frontend-skill
description: Build frontend pages, components, layouts, and styling. Use for web interfaces and UI development.
---

# Frontend Skill

## Instructions

1. **Page & Component Structure**
   - Build full pages and reusable components
   - Organize layout for responsive design
   - Implement grid and flex layouts for flexibility

2. **Styling**
   - Apply CSS, Tailwind CSS, or framework-based styling
   - Maintain consistent color schemes, fonts, and spacing
   - Support dark/light modes and theming

3. **Visual Elements & Interactivity**
   - Implement buttons, forms, modals, cards, and other UI elements
   - Add animations and transitions for smooth UX
   - Ensure accessibility and ARIA compliance

4. **Integration & Best Practices**
   - Keep code modular and reusable
   - Follow mobile-first design principles
   - Optimize frontend performance and loading speed

## Best Practices
- Use semantic HTML elements
- Keep components small and reusable
- Test responsiveness across devices
- Avoid inline styles when possible

## Example Usage
```javascript
// Example usage of Frontend Skill
frontend_skill.create_page("HomePage", layout="grid")
frontend_skill.create_component("Navbar", props=["links", "logo"])
frontend_skill.apply_styling(component="Button", styles={"color": "blue", "padding": "10px"})
frontend_skill.add_animation(component="Card", type="fade-in", duration="0.5s")
