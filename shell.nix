let pkgs = import (builtins.fetchTarball {
      url = "https://github.com/NixOS/nixpkgs/archive/77cdb1f64f9e365e41beb61f1683948e6261152c.tar.gz";
      sha256 = "1q7pmzkyqhvyg2h9qgbh7zdbvgz32nrgy8r8wrd9pvzzq981w70h";
    }) { };
in
pkgs.mkShell {
  buildInputs = [
    pkgs.vagrant
    pkgs.ansible

    # keep this line if you use bash
    pkgs.bashInteractive
  ];
}
