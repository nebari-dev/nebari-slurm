{
  description = "QHub HPC";

  inputs = {
    nixpkgs = { url = "github:nixos/nixpkgs/nixpkgs-unstable"; };
  };

  outputs = inputs@{ self, nixpkgs, ... }: {
    devShell.x86_64-linux =
      let
        pkgs = import nixpkgs { system = "x86_64-linux"; };
        pythonPackages = pkgs.python3Packages;
      in pkgs.mkShell {
        buildInputs = [
          pkgs.vagrant
          pkgs.ansible

          # development
          pythonPackages.sphinx
        ];
      };
  };
}
