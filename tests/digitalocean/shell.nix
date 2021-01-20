{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.doctl
    pkgs.terraform_0_13

    # keep this line if you use bash
    pkgs.bashInteractive
  ];

  shellHook = ''
    export DIGITALOCEAN_TOKEN=$(gopass show www/digitalocean.com/costrouchov@quansight.com qhub-terraform)
  '';
}
