{ pkgs ? import <nixpkgs> {} }:
let
  icsNoCheck = pkgs.python3Packages.ics.overridePythonAttrs (old: {
    doCheck = false;
  });
in
pkgs.mkShell {
  buildInputs = [
    (pkgs.python313.withPackages (ps: with ps; [
      ics
    ]))
  ];
}
