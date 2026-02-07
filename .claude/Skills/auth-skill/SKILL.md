---
name: auth-skill
description: Handle secure user authentication flows including signup, signin, password hashing, JWT tokens, and integration with authentication systems.
---

# Auth Skill

## Instructions

1. **User Signup & Signin**
   - Implement secure user registration (signup)
   - Enable user login (signin) with validation
   - Ensure passwords are never stored in plain text

2. **Password Security**
   - Use strong hashing algorithms (e.g., bcrypt, Argon2)
   - Validate password strength and complexity
   - Support password reset and recovery securely

3. **Token-Based Authentication**
   - Generate and verify JWT tokens for session management
   - Set appropriate token expiration and refresh strategies
   - Securely store and validate tokens on the server

4. **Integration & Best Practices**
   - Integrate easily with other authentication flows
   - Prevent brute-force and credential stuffing attacks
   - Follow security standards for web applications

## Best Practices
- Never expose passwords or sensitive data in logs or responses
- Use HTTPS for all authentication requests
- Limit login attempts and monitor suspicious activity
- Keep authentication code modular for reusability

## Example Usage
```python
# Example usage of Auth Skill
auth_skill.signup(username="newUser", password="StrongPass123!", email="user@example.com")
auth_skill.signin(username="existingUser", password="securePassword!")
auth_skill.hash_password("MySecretPass")
auth_skill.generate_jwt(user_id=123)
auth_skill.verify_jwt(token="eyJhbGciOiJIUzI1NiIsInR...")
