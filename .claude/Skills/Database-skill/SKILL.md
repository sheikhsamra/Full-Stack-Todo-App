---
name: database-skill
description: Handle database operations including creating tables, migrations, and schema design. Use for building and managing relational or NoSQL databases.
---

# Database Skill

## Instructions

1. **Schema Design**
   - Design efficient and normalized database schemas
   - Define tables, columns, relationships, and constraints
   - Ensure data integrity and consistency

2. **Table Management**
   - Create tables and define primary/foreign keys
   - Update or modify tables as per application requirements
   - Handle indexes and performance optimization

3. **Migrations**
   - Implement database migrations for version control
   - Support rolling back and applying changes safely
   - Ensure smooth schema updates without data loss

4. **Integration & Best Practices**
   - Integrate with backend code and ORMs (e.g., SQLAlchemy, Prisma)
   - Use consistent naming conventions
   - Ensure security and prevent SQL injection

## Best Practices
- Keep table designs normalized to reduce redundancy
- Index columns that are frequently queried
- Backup databases before migrations
- Use transactions for batch operations

## Example Usage
```python
# Example usage of Database Skill
db_skill.create_table("users", columns=["id INT PRIMARY KEY", "username VARCHAR(50)", "email VARCHAR(100)"])
db_skill.create_migration("add_password_column_to_users")
db_skill.update_schema("ALTER TABLE users ADD COLUMN password_hash VARCHAR(255)")
db_skill.define_relationship("users", "orders", relation_type="one-to-many")
