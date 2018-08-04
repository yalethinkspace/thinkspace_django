# Overview

## Ask yourself:

1. Am I designing an entirely new page corresponding to a Flask view/route?
2. Am I designing a small, self-contained component e.g. navbar?

If the latter, go to the `components` folder, and read the `README.md` there.

## Still here?

When designing a template, you want to start with making a copy of `skeleton.html`.

Inside, you'll find a lean skeleton code. The code *extends* `layout.html`, which means that imports, headers, navbars, footers etc. have already been taken care of. You can start writing your own custom HTML code right away.

Other tips/guidelines:

1. Import static resources like this: `<img src="{{url_for('client.static',filename='img/footer.png')}}">`
2. Import components like this: `{% from "components/navbar.html" import navbar %}`
3. Use components in code like this: `{{ navbar() }}`. (A component is a function, so the round brackets are important).
4. Do NOT write inline CSS. All CSS should go in the static `css` folder. Write CSS in new files if you need to, and make sure to import these files inside `components/imports.html` when you are done. This ensures the CSS shows up inside `layout.html` and accordingly, all the templates that depend on it.
5. Do not use `<br>` and `<hr>` if you can help it. Instead, use CSS.
6. Use the [Pesticide CSS](https://pesticide.io/) Chrome extension to visualize the DOM layout.

