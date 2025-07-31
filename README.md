# react-fastapi-starter-template

This is a template for a full stack web app that uses React for the frontend, and fastapi on the backend.
\
It is designed to help me get up and running quickly with a new project, and save time on boilerplate code.
\
\
Here's a list of the technologies used in this template:

- **Frontend**
  - [React](https://react.dev/)
  - [Shadcn UI](https://ui.shadcn.com/)
  - [Tailwind CSS](https://tailwindcss.com/)
  - [TanStack Router](https://tanstack.com/router/latest)
  - [TanStack Query](https://tanstack.com/query/latest)

- **Backend**
  - [FastAPI](https://fastapi.tiangolo.com/)
  - [SQLAlchemy](https://pypi.org/project/SQLAlchemy/)
  - [PostgreSQL](https://www.postgresql.org/)

---

The `frontend/` template was created using the following commands:

```sh
pnpm create vite@latest frontend -- --template react-ts
```

And the following options in the interactive prompt

```sh
◇  Select a framework:
│  React
│
◇  Select a variant:
│  TanStack Router ↗
┌  Let's configure your TanStack application
│
◇  Select the router type:
│  File Router - File-based routing structure
│
◇  Would you like to use Tailwind CSS?
│  Yes
│
◇  Select toolchain
│  None
│
◇  What add-ons would you like for your project?
│  Form, Shadcn, Query
│
◇  Would you like any examples?
│  none
```

Additional frontend setup was done using the following commands:

```sh
cd frontend
pnpm add -D @types/node
pnpm add @tanstack/react-router @tanstack/react-router-devtools
pnpm add -D @tanstack/router-plugin
pnpm add -D prettier prettier-plugin-tailwindcss
```
