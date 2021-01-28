# Panel Dashboarding

Currently the simplest solution
[jupyter-panel-proxy](https://github.com/holoviz/jupyter-panel-proxy)
is being used which exposes all jupyter notebooks that are panel
applications in your home directory. Not recursive so it will have to
be in your current directory. Also the panel applications do not
reload unless you restart your jupyterlab server.

Panel applications can be visited going to
`/user/<username>/panel`. Your jupyterlab url should look something
like `/user/<username>/lab`.

With some additional work it should be easy enough to expose
additional directories for panel to serve.
