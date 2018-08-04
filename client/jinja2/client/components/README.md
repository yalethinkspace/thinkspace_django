# Overview

Jinja2 macros can be used to build reusable components that can be plugged into HTML templates. Think navbars, footers, avatar blocks, so on so forth...

When developing a component, you'll want to test how it looks. But you'll need access to a Flask route, and the necessary Bootstrap imports for that. So to get around that, there is a test component route that only works during development.

You can access this route at `/test-components`.

The template for this is at `components/test.html`, and you can import and plug in your components there. Cheers!

Other tips:

1. Create components like this: `{% macro navbar() -%} Your HTML here {%- endmacro %}`

You may also find the tips inside `templates/README.md` useful.