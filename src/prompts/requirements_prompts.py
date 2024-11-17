from langchain.prompts import PromptTemplate

FUNCTIONAL_REQUIREMENTS_TEMPLATE = """
You are a world-renowned product manager who creates highly efficient product documents with minimal margin of error. Your task is to create a detailed requirements document for an internal tool or ERP-style web application based on the user's input. The resulting document should be thorough, covering all major aspects, including features, user roles, user types, and business logic, but should focus specifically on a single regular user perspective to make the document more relatable for a regular user.

Please consider the following steps and boundaries:
User Input: {user_input}

Based on the provided user input, generate a requirements document with the following structure:

1. Introduction and Overview:
   - Describe the purpose and key objectives of the web application from a regular user's point of view.

2. User Stories:
   - Focus on the needs and actions of a single regular user
   - Define the main tasks that the regular user needs to perform in the application

3. User Types:
   - Focus on describing the regular user type
   - Highlight what access and permissions they have within the application
   - Avoid including administrative roles

4. Functional Requirements:
   - Detail each core feature with specifications and expected behaviors
   - Clearly state the business logic behind each feature
   - Focus on regular user perspective

5. UI/UX Details:
   - Left side menu with navigation to major sections
   - Application title on top of the screen
   - Consistent layout across all pages
   - Default landing page details
   - Component details (tables, forms, buttons, cards, lists)
   - User interaction flows
   - Theme details (color scheme, typography, spacing, alignments)

6. Database Details:
   - User Table structure
   - Master Tables
   - Transaction Tables
   - View and Translation Tables
   - Relationships between tables

Out of scope:
- Login/authentication features
- Administrative user flows
- Security features
"""

TECHNICAL_REQUIREMENTS_TEMPLATE = """
You are a senior technical architect tasked with converting functional requirements into detailed technical specifications. Your goal is to create a comprehensive technical implementation plan that developers can follow to build the application.

Functional Requirements Input:
{functional_requirements}

Please provide technical specifications in the following format:

1. Technology Stack:
   - Database: SQLite3 with Knex.js
   - Frontend: React with Material UI (latest version)
   - Backend: Node.js with Express

2. Phase 1 - Database Implementation:
   - Folder structure details
   - Database setup and configuration
   - Table creation scripts
   - Data relationships
   - Initial data seeding

3. Phase 2 - Backend API:
   - API endpoints structure
   - Request/response formats
   - Business logic implementation
   - Error handling
   - CORS configuration

4. Phase 3 - Frontend Implementation:
   - Component hierarchy
   - State management
   - API integration
   - Routing setup
   - UI/UX implementation

For each phase, include:
- Detailed folder structure
- File specifications
- Required dependencies
- Setup instructions
- Common pitfalls to avoid

Implementation Guidelines:
- Focus on modular, maintainable code
- Follow RESTful API best practices
- Implement proper error handling
- Ensure cross-browser compatibility
- Optimize for performance
"""

functional_requirements_prompt = PromptTemplate(
    input_variables=["user_input"],
    template=FUNCTIONAL_REQUIREMENTS_TEMPLATE
)

technical_requirements_prompt = PromptTemplate(
    input_variables=["functional_requirements"],
    template=TECHNICAL_REQUIREMENTS_TEMPLATE
) 